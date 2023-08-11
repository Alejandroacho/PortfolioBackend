"""App URL Configuration"""
from Project.utils.urls import URLPathGenerator


URLGenerator: URLPathGenerator = URLPathGenerator()

urlpatterns: list = [
    *URLGenerator.prometheus_urls,
    *URLGenerator.jet_urls,
    *URLGenerator.admin_urls,
    URLGenerator.generate("Users"),
    URLGenerator.generate("Certifications"),
    URLGenerator.generate("Projects"),
    *URLGenerator.api_documentation_urls,
    *URLGenerator.media_urls,
]
