"""Project OC DAP 10 - Projects models file."""

from .models import Project
from rest_framework import serializers
from contribution.models import Contributor

# Create your models here.


class ProjectSerializer(serializers.ModelSerializer):
    """Project serializer."""

    class Meta:
        """Serializer meta properties."""

        model = Project
        fields = ["id", "title", "description", "type"]
