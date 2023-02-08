from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Images.views import ImageViewSet


router: DefaultRouter = DefaultRouter()
router.register("images", ImageViewSet, basename="images")

urlpatterns: list = [
    path("", include(router.urls)),
]
