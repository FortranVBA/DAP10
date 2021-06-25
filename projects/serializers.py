"""Project OC DAP 10 - Projects models file."""

from .models import Project
from rest_framework import serializers

# Create your models here.


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author_user"]
        extra_kwargs = {"author_user": {"required": False}}

    def create(self, validated_data):
        return Project.objects.create(**validated_data)
