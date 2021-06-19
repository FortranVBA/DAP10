"""Project OC DAP 10 - Issues models file."""

from django.db import models
from projects.models import Project
from account.models import Person

# Create your models here.


class Issue(models.Model):
    """Issue model."""

    title = models.CharField(max_length=128)
    desc = models.TextField(max_length=2048, blank=True)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project = models.ForeignKey(to=Project)
    status = models.CharField(max_length=128)
    author_user = models.ForeignKey(to=Person)
    assigned_user = models.ForeignKey(to=Person)
    created_time = models.DateTimeField(auto_now_add=True)
