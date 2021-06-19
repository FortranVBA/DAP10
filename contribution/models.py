"""Project OC DAP 10 - Contribution models file."""

from django.db import models
from account.models import Person
from projects.models import Project

# Create your models here.


class Contributor(models.Model):
    """Contributor model."""

    user = models.ForeignKey(to=Person)
    project = models.ForeignKey(to=Project)
    permission = [
        ("author", "Auteur"),
        ("contribor", "Contributeur"),
    ]
    role = models.CharField(max_length=128)
