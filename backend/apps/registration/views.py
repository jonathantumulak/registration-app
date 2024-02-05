from django.contrib.auth import (
    authenticate,
    login,
)
from django.contrib.auth.models import User
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.registration.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    @action(methods=["GET"], detail=False)
    def profile(self, request):
        if request.user.is_authenticated:
            serializer = self.serializer_class(request.user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=["POST"], detail=False)
    def login(self, request, format=None):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["POST"], detail=False)
    def register(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        if User.objects.filter(username=username).exists():
            return Response({"status": 210})

        # user creation
        user = User.objects.create_user(
            user_name=username,
            password=password,
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
