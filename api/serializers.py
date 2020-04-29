from rest_auth.models import TokenModel
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from app.models import *
from rest_framework_recursive.fields import RecursiveField


class PostAllSerializer(serializers.ModelSerializer):
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
    published_date = serializers.DateTimeField(default=timezone.now)
    in_favorite = serializers.SerializerMethodField(read_only=True)
    in_cart = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Goods
        fields = ('__all__')

    def get_in_favorite(self, instance):  # необходимо проверить бд под нагрузкой
            """Является ли товар в избранном у пользователя"""
            user = self.context['request'].user
            try:
                fav = FavoriteGood.objects.get(good=instance, client=user)
                if fav is not None:
                    return True
            except:
                pass
            return False

    def get_in_cart(self, instance):
            user = self.context['request'].user
            try:
                cart = GoodsInCart.objects.get(cart__customer=user, cart__accepted=False, good=instance)
                if cart is not None:
                    return True
            except:
                pass
            return False


class ChildCommentSerializer(serializers.ModelSerializer):
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
    author = serializers.CharField()
    child_comment = ChildCommentSerializer(many=True)
    class Meta:
        model = Comment
        fields = ('__all__')


class CommentAllSerializer(serializers.ModelSerializer):
    child_comment = ChildCommentSerializer(read_only=True, many=True)
    class Meta:
        model = Comment
        fields = ('__all__')


class CategoryParentSerializer(serializers.ModelSerializer):
    """Сериализаци родителя категории"""
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategoryListSerializer(serializers.ModelSerializer):
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
    edit_date = serializers.DateTimeField(default=timezone.now, read_only=True)
    #published_date = serializers.DateTimeField(default=timezone.now)
    created_date = serializers.DateTimeField(default=timezone.now, read_only=True)

    class Meta:
        model = Post
        fields = (
            #'author',
            'title',
            'category',
            'text',
            'slug',
            'created_date',
            'edit_date',
            #'published_date',
            'published',
            'status',
        )


class PostOpsSerializer(serializers.ModelSerializer):
    #edit_date = serializers.DateTimeField(default=timezone.now, read_only=True)
    author = serializers.CharField()
    category = serializers.CharField()
    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'category',
            'text',
            'image',
            'slug',
            #'edit_date',
            #'published_date',
            'published',
            'status',
        )


class GoodsListSerializer(serializers.ModelSerializer):
    in_cart = serializers.SerializerMethodField(read_only=True)
    in_favorite = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Goods
        fields = (
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

    def get_in_favorite(self, instance):# необходимо проверить бд под нагрузкой
        """Является ли товар в избранном у пользователя"""
        user = self.context['request'].user
        try:
            fav = FavoriteGood.objects.get(good=instance, client=user)
            if fav is not None:
                return True
        except:
            pass
        return False

    def get_in_cart(self, instance):
        user = self.context['request'].user
        try:
            cart = GoodsInCart.objects.get(cart__customer=user, cart__accepted=False, good=instance)
            if cart is not None:
                return True
        except:
            pass
        return False


class GoodsByCategorySerializer(serializers.ModelSerializer):
    in_cart = serializers.SerializerMethodField(read_only=True)
    in_favorite = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Goods
        fields = (
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

    def get_in_favorite(self, instance):  # необходимо проверить бд под нагрузкой
            """Является ли товар в избранном у пользователя"""
            user = self.context['request'].user
            try:
                fav = FavoriteGood.objects.get(good=instance, client=user)
                if fav is not None:
                    return True
            except:
                pass
            return False

    def get_in_cart(self, instance):
            user = self.context['request'].user
            try:
                cart = GoodsInCart.objects.get(cart__customer=user, cart__accepted=False, good=instance)
                if cart is not None:
                    return True
            except:
                pass
            return False


class GoodsDescriptionInCartSerializer(serializers.ModelSerializer):
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
    amount = serializers.IntegerField(read_only=True)
    good = GoodsDescriptionInCartSerializer()
    class Meta:
        model = GoodsInCart
        fields = ('__all__')

class PostGoodsInCartSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = GoodsInCart
        fields = ('__all__')


class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('__all__')


class CartSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Cart
        fields = ('__all__')


class FavoriteGoodsListSerializer(serializers.ModelSerializer):
    good = GoodsListSerializer(many=True)

    class Meta:
        model = FavoriteGood
        fields = ('__all__')


class FavoriteGoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteGood
        fields = ('good',)


class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    accepted = serializers.BooleanField(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('__all__')


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'date', 'amount',)


class UserDetailInLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class LoginSerializer(serializers.ModelSerializer):
    user = UserDetailInLoginSerializer()
    class Meta:
        model = TokenModel
        fields = ('key', 'user',)








