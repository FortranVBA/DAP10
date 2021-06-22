from projects.models import Project
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from contribution.models import Contributor
from account.serializers import PersonSerializer

# Create your views here.


class ProjectContributors(APIView):
    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        project = self.get_project(id)

        if Contributor.objects.filter(user=request.user, project=project):
            contributors = Contributor.objects.filter(project=project)

            persons = [contributor.user for contributor in contributors]
            serializer = PersonSerializer(persons, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
