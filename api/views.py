from rest_framework import generics, permissions
from app.models import *
from .serializers import *
from rest_framework.mixins import CreateModelMixin


class PostList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostAllSerializer


class CategoryList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategoryAllSerializer


class GoodsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Goods.objects.all()
    serializer_class = GoodsAllSerializer


class CommentList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Comment.objects.all()
    serializer_class = CommentAllSerializer


class GoodsOperations(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Goods.objects.all()
    lookup_field = 'id'
    serializer_class = GoodsListSerializer


class CatList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryOperations(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    lookup_field = 'id'
    serializer_class = CategoryOpsSerializer


class CategoryCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategoryOpsSerializer


class PostCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostOperations(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
    lookup_field = 'id'
    serializer_class = PostOpsSerializer





