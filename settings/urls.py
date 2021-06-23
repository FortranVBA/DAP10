"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from projects.views import ProjectView, ProjectDetails
from account.views import SignUpView
from contribution.views import ProjectContributors, DeleteContributor
from issues.views import IssueView, IssueEditView

from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("projects/", ProjectView.as_view()),
    path("projects/<int:id>/", ProjectDetails.as_view()),
    path("projects/<int:id>/issues/", IssueView.as_view()),
    path("projects/<int:id>/issues/<int:issue_id>/", IssueEditView.as_view()),
    path("projects/<int:id>/users/", ProjectContributors.as_view()),
    path("projects/<int:id>/users/<int:user_id>/", DeleteContributor.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("signup/", SignUpView.as_view()),
    path("admin/", admin.site.urls),
]
