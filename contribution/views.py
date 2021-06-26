from projects.models import Project
from account.models import Person
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from contribution.models import Contributor
from account.serializers import PersonSerializer
from .serializers import ContributorSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class IsAuthor(permissions.BasePermission):
    message = "You cannot remove the author of this project."

    def has_object_permission(self, request, view, obj):
        return not obj.permission == "author"


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

    permission_classes = [IsAuthor]

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

        user_deleted = self.get_user(user_id)
        if Contributor.objects.filter(user=user_deleted, project=project):

            contribution_deleted = Contributor.objects.filter(
                user=user_deleted, project=project
            )[0]

            self.check_object_permissions(self.request, contribution_deleted)

            Contributor.objects.filter(user=user_deleted, project=project).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ContributionViewSet(viewsets.ViewSet):
    def get_project(self, id):
        try:
            return Project.objects.get(id=id)

        except Project.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, projects_pk):
        project = self.get_project(projects_pk)

        contributors = Contributor.objects.filter(project=project)

        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def create(self, request, projects_pk):

        data = request.data.copy()
        data["user"] = Person.objects.get(username=data["user"]).id
        serializer = ContributorSerializer(data=data)
        if serializer.is_valid():
            serializer.save(permission="contributor", role="Contributor")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, projects_pk, pk=None):
        contributor = Contributor.objects.get(id=pk)

        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
