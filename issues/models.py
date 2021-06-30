"""Project OC DAP 10 - Issues models file."""

from django.db import models
from projects.models import Project
from account.models import Person

# Create your models here.


class Issue(models.Model):
    """Issue model."""

    TAG_CHOICES = [
        ("bug", "bug"),
        ("improvement", "amélioration"),
        ("task", "tâche"),
    ]

    PRIORITY_CHOICES = [
        ("low", "basse"),
        ("medium", "moyenne"),
        ("high", "haute"),
    ]

    STATUS_CHOICES = [
        ("to_do", "à faire"),
        ("on_going", "en cours"),
        ("done", "terminé"),
    ]

    title = models.CharField(max_length=128)
    desc = models.TextField(max_length=2048, blank=True)
    tag = models.CharField(
        max_length=128,
        choices=TAG_CHOICES,
        default="bug",
    )
    priority = models.CharField(
        max_length=128,
        choices=PRIORITY_CHOICES,
        default="low",
    )
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=128,
        choices=STATUS_CHOICES,
        default="to_do",
    )
    author_user = models.ForeignKey(
        to=Person, on_delete=models.CASCADE, related_name="author"
    )
    assigned_user = models.ForeignKey(
        to=Person, on_delete=models.CASCADE, related_name="assigned"
    )
    created_time = models.DateTimeField(auto_now_add=True)
