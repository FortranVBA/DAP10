"""Project OC DAP 10 - Account models file."""

from django.contrib.auth.models import User

# Create your models here.


class Person(User):
    """Person model (extend User model)."""

    class Meta:
        """Model meta properties."""

        proxy = True
