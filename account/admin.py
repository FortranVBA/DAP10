"""Project OC DAP 10 - Account admin file."""

from django.contrib import admin
from .models import Person

# Register your models here.
admin.site.register(Person)
