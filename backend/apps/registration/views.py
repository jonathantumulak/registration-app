from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.registration.serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    http_method_names = ["get", "post", "put"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "login":
            return UserLoginSerializer
        return UserSerializer

    @action(methods=["POST"], detail=False)
    def login(self, request, format=None):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"], password=serializer.validated_data["password"]
            )
            if user:
                login(request, user)
                user_serializer = UserSerializer(instance=user)
                return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["GET"], detail=False)
    def session(self, request, format=None):
        if request.user.is_authenticated:
            return Response(
                {"is_authenticated": request.user.is_authenticated, "user_id": request.user.id},
                status=status.HTTP_200_OK,
                headers={"X-CSRFToken": get_token(request)},
            )
        return Response({"is_authenticated": False}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def logout(self, request, format=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_404_NOT_FOUND)
        logout(request)
        return Response(status=status.HTTP_200_OK)
