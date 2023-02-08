from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Certifications.views import CertificationViewSet


router: DefaultRouter = DefaultRouter()
router.register(
    "certifications", CertificationViewSet, basename="certifications"
)

urlpatterns: list = [
    path("", include(router.urls)),
]
