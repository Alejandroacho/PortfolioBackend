from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Users.views import UserViewSet


router: DefaultRouter = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns: list = [
    path("", include(router.urls)),
]
