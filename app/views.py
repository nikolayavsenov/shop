from django.shortcuts import render
from rest_framework import generics, permissions
from mag.app.models import *
from mag.api.serializers import *


class PostList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
