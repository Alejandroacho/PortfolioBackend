from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import RedirectView
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.views import APIView


class URLPathGenerator:
    @staticmethod
    def generate(app_name: str, root_path: str = "api/") -> str:
        urls: tuple = (f"{app_name}.urls", app_name)
        return path(root_path, include(urls, namespace=f"{app_name.lower()}"))

    @property
    def prometheus_urls(self) -> list:
        django_prometheus_urlpatterns: list = [
            path(
                "", include("django_prometheus.urls"), name="django-prometheus"
            ),
            path("prometheus/", include("django_prometheus.urls")),
        ]
        return django_prometheus_urlpatterns

    @property
    def jet_urls(self) -> list:
        jet_urlpatterns: list = [
            path("jet/", include("jet.urls", "jet")),
            path(
                "jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")
            ),
        ]
        return jet_urlpatterns

    @property
    def admin_urls(self) -> list:
        admin_urlpatterns: list = [path("admin/", admin.site.urls)]
        return admin_urlpatterns

    @property
    def api_documentation_urls(self) -> list:
        api_schema: APIView = SpectacularAPIView.as_view()
        swagger: APIView = SpectacularSwaggerView.as_view(url_name="schema")
        redoc: APIView = SpectacularRedocView.as_view(url_name="schema")
        api_documentation_urlpatterns: list = [
            path("api/schema/", api_schema, name="schema"),
            path("docs/swagger/", swagger, name="swagger-ui"),
            path("docs/redoc/", redoc, name="redoc"),
        ]
        return api_documentation_urlpatterns

    @property
    def media_urls(self) -> list:
        favicon_url: str = staticfiles_storage.url("favicon.ico")
        favicon_view: APIView = RedirectView.as_view(url=favicon_url)
        media_urlpatterns: list = [
            path("favicon.ico", favicon_view),
            re_path(
                r"media/(?P<path>.*)$",
                serve,
                {"document_root": settings.MEDIA_ROOT},
            ),
        ]
        return media_urlpatterns
