from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    registered_at = serializers.DateTimeField(format="%H:%M %d.%m.%Y", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "registered_at"]
