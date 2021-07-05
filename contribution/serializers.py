"""Project OC DAP 10 - Projects models file."""

from .models import Contributor
from projects.models import Project
from account.models import Person
from rest_framework import serializers

# Create your models here.


class ContributorSerializer(serializers.ModelSerializer):
    """Contributor serializer."""

    class Meta:
        """Serializer meta properties."""

        model = Contributor
        fields = ["id", "user", "project", "permission", "role"]
        extra_kwargs = {
            "permission": {"required": False},
            "role": {"required": False},
            "user": {"read_only": True},
            "project": {"read_only": True},
        }

    def create(self, validated_data):
        """Add contributor."""
        path_issue = str(self.context["request"].path).split("/projects/")[1]
        projects_pk = int(path_issue.split("/")[0])

        validated_data["user"] = Person.objects.get(
            username=self.context["request"].data["username"]
        )
        validated_data["project"] = Project.objects.get(id=projects_pk)

        return super().create(validated_data)
