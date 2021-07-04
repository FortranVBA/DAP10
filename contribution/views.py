from projects.models import Project
from account.models import Person
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Contributor
from .serializers import ContributorSerializer
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


class ContributionViewSet(viewsets.ViewSet):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "destroy":
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated, IsContributorOrAuthor]

        return [permission() for permission in permission_classes]

    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return None

    def get_contributor(self, id):
        try:
            return Contributor.objects.get(id=id)

        except Contributor.DoesNotExist:
            return None

    def list(self, request, projects_pk):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        contributors = Contributor.objects.filter(project=project)

        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def create(self, request, projects_pk):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        data = request.data.copy()
        data["user"] = Person.objects.get(username=data["user"]).id
        data["project"] = projects_pk
        serializer = ContributorSerializer(data=data)
        if serializer.is_valid():
            serializer.save(permission="contributor", role="Contributor")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, projects_pk, pk=None):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        contributor = self.get_contributor(pk)
        if not contributor:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        if not contributor.permission == "author":
            contributor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ContributionModelsViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        path_issue = str(self.request.path).split("/projects/")[1]
        projects_pk = int(path_issue.split("/")[0])

        return Contributor.objects.filter(project=projects_pk)
