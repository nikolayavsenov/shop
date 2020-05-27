from rest_auth.models import TokenModel
from rest_framework import serializers
from app.models import *
from rest_framework_recursive.fields import RecursiveField


def in_favorite(context, obj):
    """Является ли товар в избранном у пользователя"""
    return obj.id in context['favorite_goods']


def in_cart(context, obj):
    """Является ли товар в корзине у пользователя"""
    return obj.id in context['cart_goods']


class PostAllSerializer(serializers.ModelSerializer):
    """Вывод всех постов"""
    author = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'short_text',
            'image',
            'published',
            'viewed',
            'status',
            'sort',
            'author',
            'category',
                  )


class GoodsAllSerializer(serializers.ModelSerializer):
    """Вывод всех товаров"""
    published_date = serializers.DateTimeField(default=timezone.now, allow_null=True)
    in_favorite = serializers.SerializerMethodField(read_only=True, default=False)
    in_cart = serializers.SerializerMethodField(read_only=True, default=False)

    class Meta:
        model = Goods
        fields = '__all__'

    def get_in_favorite(self, obj):
                return in_favorite(self.context, obj)

    def get_in_cart(self, obj):
            return in_cart(self.context, obj)


class ChildCommentSerializer(serializers.ModelSerializer):
    """Дочерний комментарий"""
    author = serializers.CharField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'created_date',
        )


class CommentOpsSerializer(serializers.ModelSerializer):
    """Редактирование комментариев"""
    author = serializers.CharField()
    child_comment = ChildCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentAllSerializer(serializers.ModelSerializer):
    """Все комментарии"""
    child_comment = ChildCommentSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CategoryParentSerializer(serializers.ModelSerializer):
    """Сериализаци родителя категории"""
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategoryListSerializer(serializers.ModelSerializer):
    """"Все категории"""
    parent = CategoryParentSerializer()

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'published',
            'parent',
        )


class CategoryOpsSerializer(serializers.ModelSerializer):
    """Редактирование категорий"""
    parent = RecursiveField

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'published',
            'parent'
        )


class PostCreateSerializer(serializers.ModelSerializer):
    """Создание поста"""
    edit_date = serializers.DateTimeField(default=timezone.now, read_only=True)
    created_date = serializers.DateTimeField(default=timezone.now, read_only=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'category',
            'text',
            'slug',
            'created_date',
            'edit_date',
            'published',
            'status',
        )


class PostOpsSerializer(serializers.ModelSerializer):
    """Редактирование поста"""
    author = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'category',
            'text',
            'image',
            'slug',
            'published',
            'status',
        )


class GoodsListSerializer(serializers.ModelSerializer):
    """Список товаров"""
    in_cart = serializers.SerializerMethodField(read_only=True)
    in_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Goods
        fields = (
            'id',
            'name',
            'in_cart',
            'in_favorite',
            'manufacturer',
            'issue_year',
            'sort',
            'published_date',
            'photo',
            'left',
            'description',
            'price',
            'discount',
            'category',
            'slug',
        )

    def get_in_favorite(self, obj):
            return in_favorite(self.context, obj)

    def get_in_cart(self, obj):
            return in_cart(self.context, obj)


class GoodsByCategorySerializer(serializers.ModelSerializer):
    """Товары по категориям"""
    in_cart = serializers.SerializerMethodField(read_only=True)
    in_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Goods
        fields = (
            'id',
            'name',
            'in_cart',
            'in_favorite',
            'manufacturer',
            'issue_year',
            'sort',
            'published_date',
            'photo',
            'left',
            'description',
            'price',
            'discount',
            'category',
            'slug',
        )

    def get_in_favorite(self, obj):
            return in_favorite(self.context, obj)

    def get_in_cart(self, obj):
            return in_cart(self.context, obj)


class GoodsDescriptionInCartSerializer(serializers.ModelSerializer):
    """Описание товаров в корзине"""
    photo = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Goods
        fields = (
            'id',
            'name',
            'short_text',
            'price',
            'photo',
        )


class GoodsInCartSerializer(serializers.ModelSerializer):
    """Список товаров в корзине"""
    good = GoodsDescriptionInCartSerializer()

    class Meta:
        model = GoodsInCart
        fields = ('amount', 'good', 'quantity',)
        read_only_fields = ('amount', 'good', )


class EditGoodsInCartSerializer(serializers.ModelSerializer):
    """Редактирование количества товаров в корзине"""
    class Meta:
        model = GoodsInCart
        fields = ('amount', 'good', 'quantity',)
        read_only_fields = ('amount', 'good',)


class PostGoodsInCartSerializer(serializers.ModelSerializer):
    """Добавление товара в корзину"""

    class Meta:
        model = GoodsInCart
        fields = '__all__'
        read_only_fields = ('amount', 'cart',)


class PromoCodeInCartSerializer(serializers.ModelSerializer):
    """Информация о промо-коде в корзине"""
    class Meta:
        model = PromoCode
        fields = ('id', 'name', 'description', 'discount_value',)


class CartListSerializer(serializers.ModelSerializer):
    """Полная информация по корзине"""
    promo_code = PromoCodeInCartSerializer()
    goods = GoodsInCartSerializer(many=True, source='get_goods')

    class Meta:
        model = Cart
        fields = ('promo_code', 'amount_items', 'promo_price', 'goods',)


class CartSerializer(serializers.ModelSerializer):
    """Список корзин"""
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['customer']


class FavoriteGoodsListSerializer(serializers.ModelSerializer):
    """Избранные товары"""
    good = GoodsListSerializer()

    class Meta:
        model = FavoriteGood
        fields = '__all__'


class FavoriteGoodCreateSerializer(serializers.ModelSerializer):
    """Добавление товара в избранное"""
    class Meta:
        model = FavoriteGood
        fields = ['good']


class PromoCodeSerializer(serializers.ModelSerializer):
    """Добавление промо-кода"""
    class Meta:
        model = PromoCode
        fields = ["name"]


class OrderSerializer(serializers.ModelSerializer):
    """Создание заказа"""
    accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'amount',
            'date',
            'accepted',
            'cart',
            'comment',
            'receiver_name',
            'is_save_info',
            'delivery_address',
            'receiver_surname',
            'receiver_mail',
        )
        read_only_fields = ('amount', 'date', 'accepted', 'cart', )


class OrderHistorySerializer(serializers.ModelSerializer):
    """История заказов"""
    promo_code = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ('id', 'date', 'amount', 'promo_code')


class UserDetailInLoginSerializer(serializers.ModelSerializer):
    """Возвращает доп. данные при логине"""
    class Meta:
        model = User
        fields = ('id', 'username',)


class LoginSerializer(serializers.ModelSerializer):
    """Кастом логин"""
    user = UserDetailInLoginSerializer()

    class Meta:
        model = TokenModel
        fields = ('key', 'user',)


class GetPromoSerializer(serializers.ModelSerializer):
    """Информация о промо-коде"""
    promo_code = serializers.SlugRelatedField(queryset=PromoCode.objects.all(), slug_field='name')

    class Meta:
        model = Cart
        fields = ('promo_code', 'amount_items', 'promo_price', )
        read_only_fields = ('amount_items', 'promo_price', )