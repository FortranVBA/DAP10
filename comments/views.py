from django.shortcuts import render

from django.shortcuts import get_object_or_404
from .serializers import CommentSerializer
from .models import Comment
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from issues.models import Issue

# Create your views here.
class CommentsViewSet(viewsets.ViewSet):
    def get_issue(self, id):
        try:
            return Issue.objects.get(id=id)

        except Issue.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get_comment(self, id):
        try:
            return Comment.objects.get(id=id)

        except Comment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, projects_pk, issues_pk):

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user=request.user, issue=self.get_issue(issues_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, projects_pk, issues_pk):
        comments = Comment.objects.filter(issue=issues_pk)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def update(self, request, projects_pk, issues_pk, pk=None):
        comment = self.get_comment(pk)

        data = request.data.copy()
        data["issue"] = issues_pk
        data["author_user"] = request.user.id
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, projects_pk, issues_pk, pk=None):
        deleted_comment = Comment.objects.get(id=pk)
        deleted_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, projects_pk, issues_pk, pk=None):
        comment = self.get_comment(pk)

        serializer = CommentSerializer(comment)
        return Response(serializer.data)
