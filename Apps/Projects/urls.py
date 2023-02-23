from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Projects.views import ProjectViewSet


router: DefaultRouter = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns: list = [
    path("", include(router.urls)),
]
