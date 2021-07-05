"""settings URL Configuration.

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

from projects.views import ProjectModelsViewSet
from contribution.views import ContributionModelsViewSet
from issues.views import IssuesModelsViewSet
from comments.views import CommentsModelsViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import SignUpView

router = DefaultRouter()
router.register(r"projects", ProjectModelsViewSet, basename="projects")

project_router = routers.NestedSimpleRouter(router, r"projects", lookup="projects")
project_router.register(r"users", ContributionModelsViewSet, basename="users")
project_router.register(r"issues", IssuesModelsViewSet, basename="issues")

issue_router = routers.NestedSimpleRouter(project_router, r"issues", lookup="issues")
issue_router.register(r"comments", CommentsModelsViewSet, basename="comments")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("login/refresh/", TokenRefreshView.as_view()),
    path("signup/", SignUpView.as_view()),
    path("admin/", admin.site.urls),
]

urlpatterns += router.urls
urlpatterns += project_router.urls
urlpatterns += issue_router.urls
