"""Project OC DAP 10 - Projects view file."""

from .models import Project
from .serializers import ProjectSerializer
from rest_framework.response import Response
from rest_framework import status
from contribution.models import Contributor
from django.db.models import Subquery
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class IsContributorOrAuthor(permissions.BasePermission):
    """Permission checking if user is a project contributor or author."""

    message = "You must be the project author or contributor."

    def has_object_permission(self, request, view, obj):
        """Check the object permission."""
        if Contributor.objects.filter(project=obj, user=request.user):
            return True
        else:
            return False


class IsAuthor(permissions.BasePermission):
    """Permission checking if user is the project author."""

    message = "You must be the project author."

    def has_object_permission(self, request, view, obj):
        """Check the object permission."""
        if Contributor.objects.filter(project=obj, user=request.user):
            permission = Contributor.objects.filter(project=obj, user=request.user)[0]
            return permission.permission == "author"
        else:
            return False


class NotAllowed(permissions.BasePermission):
    """Permission that denies all users."""

    message = "This operation is not allowed."

    def has_permission(self, request, view):
        """Check the object permission."""
        return False


class ProjectModelsViewSet(viewsets.ModelViewSet):
    """Projects viewset."""

    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Get the projects to be listed."""
        contributors = Contributor.objects.filter(user=self.request.user)
        return Project.objects.filter(id__in=Subquery(contributors.values("project")))

    def get_permissions(self):
        """Instantiate and returns the list of permissions that this view requires."""
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsContributorOrAuthor]
        elif self.action in ["update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ["list", "create", "retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [NotAllowed]

        return [permission() for permission in permission_classes]

    def create(self, request):
        """Create a project."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_project = serializer.save()

        contributor = Contributor.objects.create(
            user=request.user,
            project=new_project,
            permission="author",
            role="Creator",
        )
        contributor.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
