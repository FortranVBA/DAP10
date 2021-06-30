"""Project OC DAP 10 - Projects models file."""

from .models import Issue
from rest_framework import serializers

# Create your models here.


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
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
