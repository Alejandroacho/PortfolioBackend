from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Projects.models import Project


class ProjectAdmin(ModelAdmin):
    list_display: tuple = ("id", "title", "url")
    list_display_links: tuple = (
        "id",
        "title",
    )
    fieldsets: tuple = (
        (
            "Overview",
            {
                "fields": (
                    "id",
                    "title",
                    "description",
                    "url",
                    "is_public",
                    "repository",
                    "technologies",
                    "authors",
                    "images",
                )
            },
        ),
    )
    readonly_fields: list = ["id"]
    search_fields: tuple = ("title", "url", "id")
    ordering: tuple = ("title", "id")


admin.site.register(Project, ProjectAdmin)
