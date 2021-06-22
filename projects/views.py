from .models import Project
from .serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from contribution.models import Contributor
from django.db.models import Subquery

# Create your views here.


class ProjectView(APIView):
    """Project class based API view."""

    def get(self, request):
        contributors = Contributor.objects.filter(user=request.user)
        projects_contributed = Project.objects.filter(
            author_user__in=Subquery(contributors.values("user"))
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
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, id):
        project = self.get_project(id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        project = self.get_project(id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
