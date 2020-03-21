from rest_framework import serializers
from app.models import *


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