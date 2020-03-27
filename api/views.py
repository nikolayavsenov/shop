from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView

from app.models import *
from .serializers import *
from rest_framework.mixins import CreateModelMixin


class PostList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostAllSerializer


# class CategoryList(generics.ListAPIView):
#     permission_classes = [permissions.AllowAny]
#     queryset = Category.objects.all()
#     serializer_class = CategoryAllSerializer


class GoodsList(generics.ListCreateAPIView):
    """Список все товаров"""
    permission_classes = [permissions.IsAdminUser]
    queryset = Goods.objects.all()
    serializer_class = GoodsAllSerializer


class CommentList(generics.ListAPIView):
    """Список всех комментариев"""
    permission_classes = [permissions.AllowAny]
    queryset = Comment.objects.all()
    serializer_class = CommentAllSerializer


class GoodsOperations(generics.RetrieveUpdateDestroyAPIView):
    """Операции с товарами"""
    permission_classes = [permissions.IsAdminUser]
    queryset = Goods.objects.all()
    lookup_field = 'id'
    serializer_class = GoodsListSerializer


class CatList(generics.ListAPIView):
    """Список категорий"""
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryOperations(generics.RetrieveUpdateDestroyAPIView):
    """Операции с категориями"""
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    lookup_field = 'id'
    serializer_class = CategoryOpsSerializer


class CategoryCreate(generics.CreateAPIView):
    """Создание категорий"""
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategoryOpsSerializer


class PostCreate(generics.CreateAPIView):
    """Создание постов"""
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostOperations(generics.RetrieveUpdateDestroyAPIView):
    """Операции с постами"""
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()
    lookup_field = 'id'
    serializer_class = PostOpsSerializer


class CartList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartListSerializer
    queryset = Cart.objects.all()

    def filter_queryset(self, queryset):
        queryset = Cart.objects.filter(customer_id=self.request.user.pk)
        return queryset


class CartOps(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    lookup_field = "id"
    queryset = Cart.objects.all()

    def filter_queryset(self, queryset):
        queryset = Cart.objects.filter(customer_id=self.request.user.pk)
        return queryset




    # def get(self, request):
    #     queryset = Cart.objects.filter(customer_id=request.user.pk)
    #     serializer = CartSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = Cart.objects.filter(customer_id=request.user.pk)
    #     serializer = CartSerializer(instance, many=True, data=request.data, partial=partial)
    #     if serializer.is_valid(raise_exception=True):
    #         self.perform_update(serializer)
    #     return Response(serializer.data)
    #
    # def perform_update(self, serializer):
    #     serializer.save()
    #
    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)








