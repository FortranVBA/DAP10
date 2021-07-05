"""Project OC DAP 10 - Projects models file."""

from .models import Project
from rest_framework import serializers
from contribution.models import Contributor

# Create your models here.


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type"]
