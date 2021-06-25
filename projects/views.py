from .models import Project
from .serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from contribution.models import Contributor
from django.db.models import Subquery
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# Create your views here.


class ProjectView(APIView):
    """Project class based API view."""

    def get(self, request):
        contributors = Contributor.objects.filter(user=request.user)
        projects_contributed = Project.objects.filter(
            id__in=Subquery(contributors.values("project"))
        )

        serializer = ProjectSerializer(projects_contributed, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            new_project = serializer.save(author_user=request.user)

            contributor = Contributor.objects.create(
                user=request.user,
                project=new_project,
                permission="author",
                role="Créateur",
            )
            contributor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetails(APIView):
    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        project = self.get_project(id)

        if Contributor.objects.filter(user=request.user, project=project):
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, id):
        project = self.get_project(id)

        if Contributor.objects.filter(user=request.user, project=project):
            serializer = ProjectSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        project = self.get_project(id)

        if Contributor.objects.filter(user=request.user, project=project):
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProjectViewSet(viewsets.ViewSet):
    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

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
                role="Créateur",
            )
            contributor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        project = self.get_project(pk)

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = self.get_project(pk)

        if Contributor.objects.filter(user=request.user, project=project):
            serializer = ProjectSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
