"""Project OC DAP 10 - Projects models file."""

from django.db import models

# Create your models here.


class Project(models.Model):
    """Project model."""

    TYPE_CHOICES = [
        ("back-end", "back-end"),
        ("front-end", "front-end"),
        ("iOS", "iOS"),
        ("Android", "Android"),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    type = models.CharField(
        max_length=128,
        choices=TYPE_CHOICES,
        default="back-end",
    )
