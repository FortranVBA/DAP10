"""Project OC DAP 10 - Comments models file."""

from django.db import models
from account.models import Person
from issues.models import Issue

# Create your models here.


class Comment(models.Model):
    """Comment model."""

    description = models.TextField(max_length=2048, blank=True)
    author_user = models.ForeignKey(to=Person)
    issue = models.ForeignKey(to=Issue)
    created_time = models.DateTimeField(auto_now_add=True)
