from rest_framework import routers

from apps.registration.views import (
    InterestsViewSet,
    UserInterestsViewSet,
    UserProfileViewSet,
    UserViewSet,
)


# Settings
api = routers.DefaultRouter()
api.trailing_slash = "/?"

# Users API
api.register(r"users", UserViewSet, basename="users")
api.register(r"userprofiles", UserProfileViewSet, basename="userprofiles")
api.register(r"interests", InterestsViewSet, basename="interests")
api.register(r"user-interests", UserInterestsViewSet, basename="user-interests")
