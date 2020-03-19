from rest_framework import serializers
from app.models import *


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title',)