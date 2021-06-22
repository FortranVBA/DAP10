"""Project OC DAP 10 - Contribution models file."""

from django.db import models
from account.models import Person
from projects.models import Project

# Create your models here.


class Contributor(models.Model):
    """Contributor model."""

    PERMISSION_CHOICES = [
        ("author", "Auteur"),
        ("contributor", "Contributeur"),
    ]

    user = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(
        max_length=128,
        choices=PERMISSION_CHOICES,
        default="contributor",
    )
    role = models.CharField(max_length=128)
