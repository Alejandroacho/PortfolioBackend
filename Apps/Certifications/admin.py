from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Certifications.models import Certification


class CertificationAdmin(ModelAdmin):
    list_display: tuple = ("id", "name", "tags", "url")
    list_display_links: tuple = (
        "id",
        "name",
    )
    fieldsets: tuple = (
        (
            "Overview",
            {
                "fields": (
                    "id",
                    "name",
                    "description",
                    "tags",
                    "url",
                    "file",
                    "image",
                )
            },
        ),
    )
    readonly_fields: list = [
        "id",
    ]
    search_fields: tuple = ("name", "tags", "url", "id")
    ordering: tuple = ("tags",)


admin.site.register(Certification, CertificationAdmin)
