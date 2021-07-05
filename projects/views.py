from .models import Project
from .serializers import ProjectSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from contribution.models import Contributor
from django.db.models import Subquery
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class IsContributorOrAuthor(permissions.BasePermission):
    message = "You must be the project author or contributor."

    def has_object_permission(self, request, view, obj):
        if Contributor.objects.filter(project=obj, user=request.user):
            return True
        else:
            return False


class IsAuthor(permissions.BasePermission):
    message = "You must be the project author."

    def has_object_permission(self, request, view, obj):
        if Contributor.objects.filter(project=obj, user=request.user):
            permission = Contributor.objects.filter(project=obj, user=request.user)[0]
            return permission.permission == "author"
        else:
            return False


class ProjectViewSet(viewsets.ViewSet):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsContributorOrAuthor]
        elif self.action in ["update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return None

    def list(self, request):
        contributors = Contributor.objects.filter(user=request.user)
        projects_contributed = Project.objects.filter(
            id__in=Subquery(contributors.values("project"))
        )

        serializer = ProjectSerializer(projects_contributed, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            new_project = serializer.save()

            contributor = Contributor.objects.create(
                user=request.user,
                project=new_project,
                permission="author",
                role="Creator",
            )
            contributor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        project = self.get_project(pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, project)

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = self.get_project(pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, project)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        project = self.get_project(pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, project)

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectModelsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        contributors = Contributor.objects.filter(user=self.request.user)
        return Project.objects.filter(id__in=Subquery(contributors.values("project")))

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsContributorOrAuthor]
        elif self.action in ["update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request):
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
