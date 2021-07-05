from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Issue
from .serializers import IssueSerializer
from account.models import Person
from projects.models import Project
from contribution.models import Contributor
from rest_framework import status
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class IsProjectContributorOrAuthor(permissions.BasePermission):
    message = "You must be the project author or contributor."

    def has_object_permission(self, request, view, obj):
        return bool(Contributor.objects.filter(project=obj, user=request.user))


class IsAuthor(permissions.BasePermission):
    message = "You must be the issue author."

    def has_object_permission(self, request, view, obj):
        return obj.author_user == request.user


class IssueViewSet(viewsets.ViewSet):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated, IsProjectContributorOrAuthor]

        return [permission() for permission in permission_classes]

    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return None

    def get_issue(self, id):
        try:
            return Issue.objects.get(id=id)

        except Issue.DoesNotExist:
            return None

    def list(self, request, projects_pk):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        issues = Issue.objects.filter(project=project)

        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def create(self, request, projects_pk):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        data = request.data.copy()
        data["assigned_user"] = Person.objects.get(username=data["assigned_user"]).id
        data["project"] = project.id
        data["author_user"] = request.user.id
        serializer = IssueSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, projects_pk, pk=None):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        issue = self.get_issue(pk)
        if not issue:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, issue)

        data = request.data.copy()
        data["assigned_user"] = Person.objects.get(username=data["assigned_user"]).id
        data["project"] = project.id
        data["author_user"] = request.user.id
        serializer = IssueSerializer(issue, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, projects_pk, pk=None):
        deleted_issue = self.get_issue(pk)
        if not deleted_issue:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, deleted_issue)

        deleted_issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssuesModelsViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["projects_pk"])

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAuthor]
        else:
            permission_classes = [IsAuthenticated, IsProjectContributorOrAuthor]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs["projects_pk"])
        self.check_object_permissions(request, project)
        return super().list(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs["projects_pk"])
        self.check_object_permissions(request, project)

        return super().create(request, args, kwargs)
