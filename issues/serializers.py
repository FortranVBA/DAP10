"""Project OC DAP 10 - Projects models file."""

from .models import Issue
from projects.models import Project
from account.models import Person
from rest_framework import serializers

# Create your models here.


class IssueSerializer(serializers.ModelSerializer):
    """Issue serializer."""

    class Meta:
        """Serializer meta properties."""

        model = Issue
        fields = [
            "id",
            "title",
            "desc",
            "tag",
            "priority",
            "project",
            "status",
            "author_user",
            "assigned_user",
            "created_time",
        ]
        extra_kwargs = {
            "author_user": {"required": False},
            "project": {"required": False},
            "assigned_user": {"required": False},
        }

    def create(self, validated_data):
        """Create issue."""
        path_issue = str(self.context["request"].path).split("/projects/")[1]
        project_pk = int(path_issue.split("/")[0])

        validated_data["author_user"] = self.context["request"].user
        validated_data["project"] = Project.objects.get(id=project_pk)

        if self.context["request"].data["assigned_username"] == "":
            validated_data["assigned_user"] = self.context["request"].user
        else:
            username = self.context["request"].data["assigned_username"]
            validated_data["assigned_user"] = Person.objects.get(username=username)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update issue."""
        path_issue = str(self.context["request"].path).split("/projects/")[1]
        project_pk = int(path_issue.split("/")[0])

        validated_data["author_user"] = self.context["request"].user
        validated_data["project"] = Project.objects.get(id=project_pk)

        if self.context["request"].data["assigned_username"] == "":
            validated_data["assigned_user"] = self.context["request"].user
        else:
            username = self.context["request"].data["assigned_username"]
            validated_data["assigned_user"] = Person.objects.get(username=username)

        return super().update(instance, validated_data)
