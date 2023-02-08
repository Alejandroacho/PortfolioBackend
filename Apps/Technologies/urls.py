from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Technologies.views import TechnologyViewSet


router: DefaultRouter = DefaultRouter()
router.register("technologies", TechnologyViewSet, basename="technologies")

urlpatterns: list = [
    path("", include(router.urls)),
]
