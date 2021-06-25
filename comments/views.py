from django.shortcuts import render

from django.shortcuts import get_object_or_404
from .serializers import CommentSerializer
from .models import Comment
from rest_framework import viewsets

# Create your views here.
class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
