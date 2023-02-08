from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from SocialNetworks.views import SocialNetworkViewSet


router: DefaultRouter = DefaultRouter()
router.register(
    "social-networks", SocialNetworkViewSet, basename="social-networks"
)

urlpatterns: list = [
    path("", include(router.urls)),
]
