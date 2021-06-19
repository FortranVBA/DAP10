"""Project OC DAP 10 - Projects admin file."""

from django.contrib import admin

# Register your models here.
from .models import Project

# Register your models here.
admin.site.register(Project)
