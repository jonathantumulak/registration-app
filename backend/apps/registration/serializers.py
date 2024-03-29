from django.contrib.auth.models import User
from rest_framework import serializers

from apps.registration.models import (
    Interest,
    UserProfile,
)


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birth_date = serializers.DateField(source="profile.birth_date", input_formats=["iso-8601", "%Y-%m-%dT%H:%M:%S.%fZ"])
    gender = serializers.ChoiceField(choices=UserProfile.GENDERS, source="profile.gender")
    completed_welcome = serializers.BooleanField(source="profile.completed_welcome", default=False)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "birth_date", "gender", "completed_welcome"]

    def update(self, instance, validated_data):
        profile = validated_data.pop("profile", None)
        birth_date = profile.get("birth_date", None)
        gender = profile.get("gender", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        profile, created = UserProfile.objects.get_or_create(
            user=instance, defaults={"birth_date": birth_date, "gender": gender}
        )
        # update birthdate and gender if not created
        if not created:
            profile.birth_date = birth_date
            profile.gender = gender
            profile.save()
        return instance


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


class UserProfileSerializer(serializers.ModelSerializer):
    experience_level = serializers.ChoiceField(choices=UserProfile.EXPERIENCE_LEVELS)
    expected_salary = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = UserProfile
        fields = ["experience_level", "expected_salary"]


class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ["id", "name"]
        read_only_fields = ["name"]


class UserInterestsSerializer(serializers.ModelSerializer):
    interests = InterestsSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "interests",
        ]
        read_only_fields = ["interests"]


class UserInterestsWriteSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.all(),
        read_only=False,
        many=True,
    )

    class Meta:
        model = User
        fields = [
            "interests",
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # mark steps as completed
        if not instance.profile.completed_welcome:
            instance.profile.completed_welcome = True
            instance.profile.save()
        return instance
