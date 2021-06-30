"""Project OC DAP 10 - Projects models file."""

from .models import Comment
from rest_framework import serializers

from issues.models import Issue

# Create your models here.


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "author_user", "issue", "created_time"]
        extra_kwargs = {
            "author_user": {"required": False},
            "issue": {"required": False},
        }

    def create(self, validated_data):
        path_issue = str(self.context["request"].path).split("/issues/")[1]
        issue_pk = int(path_issue.split("/")[0])

        validated_data["author_user"] = self.context["request"].user
        validated_data["issue"] = Issue.objects.get(id=issue_pk)

        return super().create(validated_data)
