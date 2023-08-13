from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Experiences.views import ExperienceViewSet


router: DefaultRouter = DefaultRouter()
router.register("experiences", ExperienceViewSet, basename="experiences")

urlpatterns: list = [
    path("", include(router.urls)),
]
