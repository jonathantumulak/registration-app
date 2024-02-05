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
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.registration.models import (
    Interest,
    UserProfile,
)
from apps.registration.permissions import OwnUserPermission
from apps.registration.serializers import (
    InterestsSerializer,
    UserCreateSerializer,
    UserInterestsSerializer,
    UserInterestsWriteSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserSerializer,
)


class ListNotAllowedMixin:
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET", detail='Method "GET" not allowed without lookup')


class UserViewSet(ListNotAllowedMixin, viewsets.ModelViewSet):
    """Viewset for login, logout, get session, register user"""

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

    def get_permissions(self):
        if self.action in ["retrieve", "update"]:
            return [IsAuthenticated(), OwnUserPermission()]
        return super().get_permissions()

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


class UserProfileViewSet(ListNotAllowedMixin, viewsets.ModelViewSet):
    """Viewset for get and update user profile"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, OwnUserPermission]
    http_method_names = ["get", "put"]

    def get_object(self):
        """Provide related user profile instead"""
        user = super().get_object()
        obj = get_object_or_404(UserProfile, user=user)
        return obj


class InterestsViewSet(viewsets.ModelViewSet):
    """View for getting all interests"""

    queryset = Interest.objects.all()
    serializer_class = InterestsSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


class UserInterestsViewSet(ListNotAllowedMixin, viewsets.ModelViewSet):
    """Viewset for get and update user interests"""

    queryset = User.objects.all()
    serializer_class = UserInterestsSerializer
    permission_classes = [IsAuthenticated, OwnUserPermission]
    http_method_names = ["get", "put"]

    def get_serializer_class(self):
        if self.action == "update":
            return UserInterestsWriteSerializer
        return UserInterestsSerializer
