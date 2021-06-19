"""Project OC DAP 10 - Projects models file."""

from account.models import Person
from django.db import models

# Create your models here.


class Project(models.Model):
    """Project model."""

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    type = models.CharField(max_length=128)
    author_user = models.ForeignKey(to=Person)
