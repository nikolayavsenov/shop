from rest_framework import serializers
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
    class Meta:
        model = Goods
        fields = ('__all__')


class CommentOpsSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    class Meta:
        model = Comment
        fields = ('__all__')


class CommentAllSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Goods
        fields = (
            'name',
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


class GoodsByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = (
            'name',
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



