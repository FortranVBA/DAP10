"""Project OC DAP 10 - Projects models file."""

from .models import Contributor
from rest_framework import serializers

# Create your models here.


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "permission", "role"]
        extra_kwargs = {"permission": {"required": False}, "role": {"required": False}}
