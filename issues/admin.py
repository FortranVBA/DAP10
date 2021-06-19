"""Project OC DAP 10 - Issues admin file."""

from django.contrib import admin

# Register your models here.
from .models import Issue

# Register your models here.
admin.site.register(Issue)
