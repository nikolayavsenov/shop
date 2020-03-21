from rest_framework import generics, permissions
from app.models import *
from .serializers import *


class PostList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostAllSerializer


class CategoryList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategoryAllSerializer


class GoodsList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Goods.objects.all()
    serializer_class = GoodsAllSerializer


class CommentList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Comment.objects.all()
    serializer_class = CommentAllSerializer


