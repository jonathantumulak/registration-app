from rest_framework import routers

from apps.registration.views import (
    InterestsViewSet,
    UserProfileViewSet,
    UserViewSet,
)


# Settings
api = routers.DefaultRouter()
api.trailing_slash = "/?"

# Users API
api.register(r"users", UserViewSet)
api.register(r"userprofiles", UserProfileViewSet)
api.register(r"interests", InterestsViewSet)
