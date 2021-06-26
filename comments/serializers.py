"""Project OC DAP 10 - Projects models file."""

from .models import Comment
from rest_framework import serializers

# Create your models here.


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "author_user", "issue", "created_time"]
        extra_kwargs = {
            "author_user": {"required": False},
            "issue": {"required": False},
        }
