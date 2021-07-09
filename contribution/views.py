"""Project OC DAP 10 - Contribution view file."""

from projects.models import Project
from rest_framework.response import Response
from rest_framework import status
from .models import Contributor
from .serializers import ContributorSerializer
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


class IsProjectAuthor(permissions.BasePermission):
    """Permission checking if user is a project author."""

    message = "You must be the project author."

    def has_object_permission(self, request, view, obj):
        """Check the object permission."""
        if Contributor.objects.filter(project=obj, user=request.user):
            permission = Contributor.objects.filter(project=obj, user=request.user)[0]
            return permission.permission == "author"
        else:
            return False


class IsAuthor(permissions.BasePermission):
    """Permission checking if the deleted contributor is the project author."""

    message = "You cannot delete the project author."

    def has_object_permission(self, request, view, obj):
        """Check the object permission."""
        return not obj.permission == "author"


class NotAllowed(permissions.BasePermission):
    """Permission that denies all users."""

    message = "This operation is not allowed."

    def has_permission(self, request, view):
        """Check the object permission."""
        return False


class ContributionModelsViewSet(viewsets.ModelViewSet):
    """Contribution viewset."""

    serializer_class = ContributorSerializer

    def get_queryset(self):
        """Get the contributor to be listed."""
        path_issue = str(self.request.path).split("/projects/")[1]
        projects_pk = int(path_issue.split("/")[0])

        return Contributor.objects.filter(project=projects_pk)

    def get_permissions(self):
        """Instantiate and returns the list of permissions that this view requires."""
        if self.action == "destroy":
            permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ["list", "create"]:
            permission_classes = [IsAuthenticated, IsContributorOrAuthor]
        else:
            permission_classes = [NotAllowed]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Add a new contributor."""
        project = Project.objects.get(id=kwargs["projects_pk"])
        self.check_object_permissions(request, project)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(permission="contributor", role="Contributor")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """List all project contributors."""
        project = Project.objects.get(id=kwargs["projects_pk"])
        self.check_object_permissions(request, project)
        return super().list(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """Remove a contributor."""
        project = Project.objects.get(id=kwargs["projects_pk"])

        permission_project = IsProjectAuthor()

        if permission_project.has_object_permission(request, self, project):
            return super().destroy(request, args, kwargs)

        return Response(
            {"Detail": permission_project.message}, status=status.HTTP_400_BAD_REQUEST
        )
