from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Maintainers.views import MaintainerViewSet


router: DefaultRouter = DefaultRouter()
router.register("maintainers", MaintainerViewSet, basename="maintainers")

urlpatterns: list = [
    path("", include(router.urls)),
]
