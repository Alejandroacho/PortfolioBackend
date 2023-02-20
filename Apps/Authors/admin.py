from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Authors.models import Author


class AuthorAdmin(ModelAdmin):
    list_display: tuple = ("id", "first_name", "last_name")
    list_display_links: tuple = (
        "id",
        "first_name",
    )
    fieldsets: tuple = (
        (
            "Overview",
            {
                "fields": (
                    "id",
                    "first_name",
                    "last_name",
                    "social_networks",
                )
            },
        ),
    )
    readonly_fields: list = [
        "id",
    ]
    search_fields: tuple = ("first_name", "last_name", "id", "social_networks")
    ordering: tuple = ("first_name", "last_name", "id")


admin.site.register(Author, AuthorAdmin)
