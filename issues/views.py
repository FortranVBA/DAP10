"""Project OC DAP 10 - Issue view file."""

from .models import Issue
from .serializers import IssueSerializer
from projects.models import Project
from contribution.models import Contributor
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class IsProjectContributorOrAuthor(permissions.BasePermission):
    """Permission checking if user is a project contributor or author."""

    message = "You must be the project author or contributor."

    def has_object_permission(self, request, view, obj):
        """Check the object permission."""
        return bool(Contributor.objects.filter(project=obj, user=request.user))


class IsAuthor(permissions.BasePermission):
    """Permission checking if user is the issue author."""

    message = "You must be the issue author."

    def has_object_permission(self, request, view, obj):
        """Check the object permission."""
        return obj.author_user == request.user


class NotAllowed(permissions.BasePermission):
    """Permission that denies all users."""

    message = "This operation is not allowed."

    def has_permission(self, request, view):
        """Check the object permission."""
        return False


class IssuesModelsViewSet(viewsets.ModelViewSet):
    """Issue viewset."""

    serializer_class = IssueSerializer

    def get_queryset(self):
        """Get the issues to be listed."""
        return Issue.objects.filter(project=self.kwargs["projects_pk"])

    def get_permissions(self):
        """Instantiate and returns the list of permissions that this view requires."""
        if self.action in ["update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ["list", "create"]:
            permission_classes = [IsAuthenticated, IsProjectContributorOrAuthor]
        else:
            permission_classes = [NotAllowed]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """List all project issues."""
        project = Project.objects.get(id=kwargs["projects_pk"])
        self.check_object_permissions(request, project)
        return super().list(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """Create a project issue."""
        project = Project.objects.get(id=kwargs["projects_pk"])
        self.check_object_permissions(request, project)

        return super().create(request, args, kwargs)
