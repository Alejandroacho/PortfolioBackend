"""App URL Configuration"""
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic.base import RedirectView
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns: list = [
    # Django JET URLS
    path("jet/", include("jet.urls", "jet")),
    # Django JET dashboard URLS
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path("admin/", admin.site.urls),
    path("api/", include(("Users.urls", "users"), namespace="users")),
    path(
        "api/",
        include(
            ("Technologies.urls", "technologies"), namespace="technologies"
        ),
    ),
    path(
        "api/",
        include(
            ("SocialNetworks.urls", "social-networks"),
            namespace="social-networks",
        ),
    ),
    path(
        "api/",
        include(
            ("Images.urls", "images"),
            namespace="images",
        ),
    ),
    path(
        "api/",
        include(
            ("Certifications.urls", "certifications"),
            namespace="certifications",
        ),
    ),
    path("api/", include(("Authors.urls", "authors"), namespace="authors")),
    path("api/", include(("Projects.urls", "projects"), namespace="projects")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("", include("django_prometheus.urls"), name="django-prometheus"),
    re_path(
        r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}
    ),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    path("prometheus/", include("django_prometheus.urls")),
]
