from rest_framework import serializers
from app.models import *
from rest_framework_recursive.fields import RecursiveField


class PostAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')


class CategoryAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class GoodsAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('__all__')


class CommentAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')


class CategoryParentSerializer(serializers.ModelSerializer):
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