from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Authors.views import AuthorViewSet


router: DefaultRouter = DefaultRouter()
router.register("authors", AuthorViewSet, basename="authors")

urlpatterns: list = [
    path("", include(router.urls)),
]
