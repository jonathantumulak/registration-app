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

from apps.registration.serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "login":
            return UserLoginSerializer
        return UserSerializer

    @action(methods=["POST"], detail=False)
    def login(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"], password=serializer.validated_data["password"]
            )
            if user:
                login(request, user)
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["GET"], detail=False)
    def session(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"isAuthenticated": False}, status=status.HTTP_200_OK)

        return Response({"isAuthenticated": True}, status=status.HTTP_200_OK)
