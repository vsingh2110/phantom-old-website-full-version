from rest_framework import serializers

from core.serializers import BaseModelSerializer
from .models import Post

class PostListSerializer(BaseModelSerializer):
    class Meta:
        model = Post
        exclude = ('content',)

class PostDetailSerializer(BaseModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
