from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "avatar_url")
        read_only_fields = ("id", "username", "email")  # public view should not edit these

class MeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("bio", "avatar_url")  # optional profile fields

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "bio", "avatar_url")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # hash properly
        user.save()
        return user
