from rest_framework import generics, permissions
from app.models import *
from .serializers import *


class PostList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
