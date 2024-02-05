from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    registered_at = serializers.DateTimeField(format="%H:%M %d.%m.%Y", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "registered_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2"]

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]

        if User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError("Username already exists")
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        # user creation
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]
