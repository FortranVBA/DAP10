from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Issue
from .serializers import IssueSerializer
from account.models import Person
from projects.models import Project
from rest_framework import status
from django.http import HttpResponse

# Create your views here.


class IssueView(APIView):
    """Project class based API view."""

    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        project = self.get_project(id)

        issues = Issue.objects.filter(project=project)

        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        project = self.get_project(id)

        data = request.data.copy()
        data["assigned_user"] = Person.objects.get(username=data["assigned_user"]).id
        data["project"] = project.id
        data["author_user"] = request.user.id
        serializer = IssueSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueEditView(APIView):
    """Project class based API view."""

    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get_issue(self, id):
        try:
            return Issue.objects.get(id=id)

        except Issue.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, issue_id):
        project = self.get_project(id)

        deleted_issue = Issue.objects.get(id=issue_id)
        deleted_issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id, issue_id):
        project = self.get_project(id)
        issue = self.get_issue(id)

        data = request.data.copy()
        data["assigned_user"] = Person.objects.get(username=data["assigned_user"]).id
        data["project"] = project.id
        data["author_user"] = request.user.id
        serializer = IssueSerializer(issue, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
