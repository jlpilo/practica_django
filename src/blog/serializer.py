from rest_framework import serializers

from blog.models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostsListSerializer(serializers.ModelSerializer):

    #user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["title", "image", "intro", "published_date"]