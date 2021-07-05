from django.shortcuts import render

from django.shortcuts import get_object_or_404
from .serializers import CommentSerializer
from .models import Comment
from contribution.models import Contributor
from projects.models import Project
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from issues.models import Issue
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class IsProjectContributorOrAuthor(permissions.BasePermission):
    message = "You must be the project author or contributor."

    def has_object_permission(self, request, view, obj):

        if Contributor.objects.filter(project=obj, user=request.user):
            return True
        else:
            return False


class IsAuthor(permissions.BasePermission):
    message = "You must be the issue author."

    def has_object_permission(self, request, view, obj):
        return obj.author_user == request.user


class CommentsViewSet(viewsets.ViewSet):
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

    def get_comment(self, id):
        try:
            return Comment.objects.get(id=id)

        except Comment.DoesNotExist:
            return None

    def create(self, request, projects_pk, issues_pk):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        issue = self.get_issue(issues_pk)
        if not issue:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user=request.user, issue=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, projects_pk, issues_pk):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)

        issue = self.get_issue(issues_pk)
        if not issue:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(issue=issues_pk)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def update(self, request, projects_pk, issues_pk, pk=None):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        issue = self.get_issue(issues_pk)
        if not issue:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        comment = self.get_comment(pk)
        if not comment:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, comment)

        data = request.data.copy()
        data["issue"] = issues_pk
        data["author_user"] = request.user.id
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, projects_pk, issues_pk, pk=None):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        issue = self.get_issue(issues_pk)
        if not issue:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        deleted_comment = self.get_comment(pk)
        if not deleted_comment:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, deleted_comment)

        deleted_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, projects_pk, issues_pk, pk=None):
        project = self.get_project(projects_pk)
        if not project:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, project)

        issue = self.get_issue(issues_pk)
        if not issue:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        comment = self.get_comment(pk)
        if not comment:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class CommentsModelsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issues_pk"])

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
