from projects.models import Project
from account.models import Person
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from contribution.models import Contributor
from account.serializers import PersonSerializer
from .serializers import ContributorSerializer

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

    def post(self, request, id):
        project = self.get_project(id)

        if Contributor.objects.filter(user=request.user, project=project):
            data = request.data.copy()
            data["user"] = Person.objects.get(username=data["user"]).id
            serializer = ContributorSerializer(data=data)
            if serializer.is_valid():
                serializer.save(permission="contributor", role="Contributor")
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteContributor(APIView):
    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get_user(self, id):
        try:
            return Person.objects.get(id=id)

        except Person.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, user_id):
        project = self.get_project(id)

        if Contributor.objects.filter(user=request.user, project=project):
            user_deleted = self.get_user(user_id)
            if Contributor.objects.filter(user=user_deleted, project=project):
                Contributor.objects.filter(user=user_deleted, project=project).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
