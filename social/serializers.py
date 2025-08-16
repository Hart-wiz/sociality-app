from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ("id", "username", "bio", "avatar_url", "followers_count", "following_count")

class MeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("bio", "avatar_url")

class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ("id", "author", "body", "created_at", "updated_at")
    def validate_body(self, v):
        if not (1 <= len(v) <= 1000):
            raise serializers.ValidationError("Body must be 1–1000 characters.")
        return v
