from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from app.models import *
from .serializers import *
from rest_framework.mixins import CreateModelMixin
from .paginations import PostPagination
from random import sample


class PostList(generics.ListAPIView):
    """Список постов"""
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostAllSerializer
    pagination_class = PostPagination


class GoodsList(generics.ListCreateAPIView):
    """Список все товаров"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Goods.objects.all()
    serializer_class = GoodsAllSerializer
    pagination_class = PostPagination

    #def get(self, queryset):
        #permission_classes = [permissions.AllowAny]
        #serializer = GoodsAllSerializer(queryset)
        #return Response(serializer.data)


class GoodsByCategory(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GoodsByCategorySerializer
    lookup_field = 'category'
    queryset = Goods.objects.all()
    pagination_class = PostPagination

    def get_queryset(self):
        return Goods.objects.filter(category=self.kwargs['category'])


class RandomGoods(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Goods.objects.order_by('?')[:3]
    serializer_class = GoodsAllSerializer

    # def get_queryset(self):
    #     count = Goods.objects.all().count()
    #     random_ids = sample(range(1, count), 3)
    #     return Goods.objects.filter(id__in=random_ids)


class CommentList(generics.ListCreateAPIView):
    """Список всех комментариев"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentAllSerializer


class CommentOps(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentAllSerializer


class CommentsById(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentOpsSerializer
    lookup_field = 'post'

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post'])


class GoodsOperations(generics.RetrieveUpdateDestroyAPIView):
    """Операции с товарами"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    lookup_field = 'id'
    serializer_class = CategoryOpsSerializer


class CategoryCreate(generics.CreateAPIView):
    """Создание категорий"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategoryOpsSerializer


class PostCreate(generics.CreateAPIView):
    """Создание постов"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostOperations(generics.RetrieveUpdateDestroyAPIView):
    """Операции с постами"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    lookup_field = 'id'
    serializer_class = PostOpsSerializer


class CartList(generics.ListAPIView):
    """Возвращает содержимое корзины пользователя по токену"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartListSerializer
    queryset = Cart.objects.all()

    def filter_queryset(self, queryset):
        queryset = Cart.objects.filter(customer_id=self.request.user.pk)
        return queryset


class AddGoodToCart(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = GoodsInCart.objects.all()
    serializer_class = PostGoodsInCartSerializer

    def get_queryset(self):
        return GoodsInCart.objects.filter(cart__customer__pk=self.request.user.pk)

    def get(self, request):
        serializer = GoodsInCartSerializer(self.get_queryset(),
                                           many=True,
                                           context={'request': request})#Построение корректного image url
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


class GoodsInCartEdit(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    queryset = GoodsInCart.objects.all()
    serializer_class = GoodsInCartSerializer

    def get_queryset(self):
        return GoodsInCart.objects.filter(cart__customer__pk=self.request.user.pk)


class FavoriteList(generics.ListCreateAPIView):
    """Избранное по токену"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteGoodsListSerializer
    queryset = FavoriteGood.objects.all()

    def post(self, request):
        serializer = FavoriteGoodCreateSerializer(data=request.data)
        if serializer and serializer.is_valid():
            print(serializer)
            serializer.save(client_id=request.user.pk)
            return Response(status=201)
        else:
            return Response(status=404)

    def delete(self, request):
        try:
            data = request.data
            favorite_good = FavoriteGood.objects.get(good=data['good'])
            print(favorite_good)
            favorite_good.delete()
            return Response(status=204)
        except:
            return HttpResponse(status=404)

    def filter_queryset(self, queryset):
        queryset = FavoriteGood.objects.filter(client_id=self.request.user.pk)
        return queryset


class CartOps(generics.UpdateAPIView):
    """Редактирование корзины"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    lookup_field = "id"
    queryset = Cart.objects.all()

    def filter_queryset(self, queryset):
        queryset = Cart.objects.filter(customer_id=self.request.user.pk)
        return queryset










