from rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .serializers import *
from .paginations import PostPagination


def goods_context(user):
    cart_goods = []
    favorite_goods = []
    if not user.is_anonymous:
        for items in GoodsInCart.objects.values('good').filter(cart__customer=user, cart__accepted=False):
            cart_goods.append(items['good'])
        for items in FavoriteGood.objects.values('good').filter(client=user):
            favorite_goods.append(items['good'])
    return {
        'cart_goods': cart_goods,
        'favorite_goods': favorite_goods,
    }


class PostList(generics.ListAPIView):
    """Список постов"""
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all().select_related('author', 'category')
    serializer_class = PostAllSerializer
    pagination_class = PostPagination


class GoodsList(generics.ListCreateAPIView):
    """Список все товаров"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Goods.objects.all()
    serializer_class = GoodsAllSerializer
    pagination_class = PostPagination

    def get_serializer_context(self):
        return goods_context(self.request.user)


class GoodsByCategory(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GoodsByCategorySerializer
    lookup_field = 'category'
    queryset = Goods.objects.all()
    pagination_class = PostPagination

    def get_queryset(self):
        return Goods.objects.filter(category=self.kwargs['category'])

    def get_serializer_context(self):
        return goods_context(self.request.user)


class RandomGoods(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Goods.objects.order_by('?')[:3]
    serializer_class = GoodsAllSerializer

    def get_serializer_context(self):
        return goods_context(self.request.user)


class CommentList(generics.ListCreateAPIView):
    """Список всех комментариев"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentAllSerializer


class CreateSubComment(generics.CreateAPIView):
    """Список всех комментариев"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all().select_related('author')
    serializer_class = CommentAllSerializer

    def post(self, request, id):
        """Костыль для фронта, обработка комментариев родитель-дитя"""
        parent = Comment.objects.get(id=id)
        serializer = CommentAllSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        child = Comment.objects.get(id=serializer.data['id'])
        parent.child_comment.add(child)
        return Response(serializer.data, status=201)


class CommentOps(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all().select_related('author')
    serializer_class = CommentAllSerializer


class CommentsById(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all().select_related('author')
    serializer_class = CommentOpsSerializer
    lookup_field = 'post'

    def filter_queryset(self, queryset):
        return queryset.filter(post=self.kwargs['post'])


class GoodsOperations(generics.RetrieveUpdateDestroyAPIView):
    """Операции с товарами"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Goods.objects.all()
    serializer_class = GoodsListSerializer

    def get_serializer_context(self):
        return goods_context(self.request.user)


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
    queryset = Post.objects.all().select_related('author')
    lookup_field = 'id'
    serializer_class = PostOpsSerializer


class CartList(generics.ListAPIView):
    """Возвращает содержимое корзины пользователя по токену"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartListSerializer
    queryset = Cart.objects.all().prefetch_related('promo_code')

    def filter_queryset(self, queryset):
        queryset = queryset.filter(customer=self.request.user, accepted=False)
        return queryset


class AddGoodToCart(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = GoodsInCart.objects.all().select_related('good')
    serializer_class = PostGoodsInCartSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(cart__customer=self.request.user).filter(cart__accepted=False)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GoodsInCartSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        cart = Cart.objects.get(customer=self.request.user, accepted=False)
        serializer.save(cart=cart)


class GoodsInCartEdit(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'good'
    queryset = GoodsInCart.objects.all().select_related('good')
    serializer_class = GoodsInCartSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT' or 'PATCH':
            return EditGoodsInCartSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        return GoodsInCart.objects.filter(cart__customer=self.request.user,
                                          cart__accepted=False,
                                          good__id=self.kwargs['good'])

    def perform_update(self, serializer):
        serializer.save()


class FavoriteList(generics.ListCreateAPIView):
    """Избранное по токену"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteGoodsListSerializer
    queryset = FavoriteGood.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FavoriteGoodCreateSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def filter_queryset(self, queryset):
        queryset = queryset.filter(client=self.request.user.pk)
        return queryset

    def get_serializer_context(self):
        return goods_context(self.request.user)


class FavoriteDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'good'

    def get_queryset(self):
        queryset = FavoriteGood.objects.filter(client=self.request.user, good__id=self.kwargs['good'])
        return queryset


class CartOps(generics.UpdateAPIView):
    """Редактирование корзины"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    lookup_field = "id"
    queryset = Cart.objects.all().select_related('customer')

    def filter_queryset(self, queryset):
        queryset = queryset.filter(customer_id=self.request.user.pk)
        return queryset


class OrderList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        cart_id = Cart.objects.get(customer=self.request.user, accepted=False)
        new_cart = Cart.objects.create(customer=self.request.user)
        new_cart.save()
        serializer.save(cart=cart_id)


class OrderHistory(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderHistorySerializer
    queryset = Order.objects.all()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(cart__customer=self.request.user)
        return queryset


class OrderListInHistory(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoodsInCartSerializer
    lookup_field = 'id'

    def get_queryset(self):
        cart_id = Order.objects.values('cart').get(id=self.kwargs['id'])
        queryset = GoodsInCart.objects.filter(cart=cart_id['cart'])
        return queryset


class CustomLoginView(LoginView):
    """Логин"""
    def get_response_serializer(self):
        response_serializer = LoginSerializer
        return response_serializer


class GetPromo(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartListSerializer
    queryset = Cart.objects.all().select_related('promo_code')

    def filter_queryset(self, queryset):
        return self.queryset.filter(customer=self.request.user, accepted=False)

    def get_queryset(self):
        return self.queryset.first()
    
    def post(self, request):
        serializer = GetPromoSerializer(self.get_queryset(), data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user)
        return Response(status=200)















