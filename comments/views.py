"""Project OC DAP 10 - Comments view file."""

from .serializers import CommentSerializer
from .models import Comment
from contribution.models import Contributor
from projects.models import Project
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class IsProjectContributorOrAuthor(permissions.BasePermission):
    """Permission checking if user is a project contributor or author."""

    message = "You must be the project author or contributor."

    def has_object_permission(self, request, view, obj):
        """Check the object permission."""
        if Contributor.objects.filter(project=obj, user=request.user):
            return True
        else:
            return False


class IsAuthor(permissions.BasePermission):
    """Permission checking the comment author."""

    message = "You must be the comment author."

    def has_object_permission(self, request, view, obj):
        """Check the object permission."""
        return obj.author_user == request.user


class NotAllowed(permissions.BasePermission):
    """Permission that denies all users."""

    message = "This operation is not allowed."

    def has_permission(self, request, view):
        """Check the object permission."""
        return False


class CommentsModelsViewSet(viewsets.ModelViewSet):
    """Comment viewset."""

    serializer_class = CommentSerializer

    def get_queryset(self):
        """Get the comments to be listed."""
        return Comment.objects.filter(issue=self.kwargs["issues_pk"])

    def get_permissions(self):
        """Instantiate and returns the list of permissions that this view requires."""
        if self.action in ["update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAuthor]
        elif self.action in ["create", "list"]:
            permission_classes = [IsAuthenticated, IsProjectContributorOrAuthor]
        elif self.action in ["retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [NotAllowed]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """List the comments."""
        project = Project.objects.get(id=kwargs["projects_pk"])
        self.check_object_permissions(request, project)
        return super().list(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new comment."""
        project = Project.objects.get(id=kwargs["projects_pk"])
        self.check_object_permissions(request, project)
        return super().create(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific comment."""
        project = Project.objects.get(id=kwargs["projects_pk"])

        permission_project = IsProjectContributorOrAuthor()

        if permission_project.has_object_permission(request, self, project):
            return super().retrieve(request, args, kwargs)

        return Response(
            {"Detail": permission_project.message}, status=status.HTTP_400_BAD_REQUEST
        )
