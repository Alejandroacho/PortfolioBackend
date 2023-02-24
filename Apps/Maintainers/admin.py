from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Model

from Maintainers.models import Maintainer


class MaintainerAdmin(ModelAdmin):
    model: Model = Maintainer
    list_display: tuple = ("id", "first_name", "last_name", "email")
    list_display_links: tuple = ("id", "first_name")
    list_filter: tuple = ("first_name", "last_name", "email")
    fieldsets: tuple = (
        (
            "Overview",
            {
                "fields": (
                    "id",
                    "first_name",
                    "last_name",
                    "email",
                    "about",
                    "cv",
                    "certifications",
                    "images",
                    "social_networks",
                    "author",
                )
            },
        ),
    )
    readonly_fields: list = ["id"]
    search_fields: tuple = ("email", "last_name", "first_name", "id")


admin.site.register(Maintainer, MaintainerAdmin)
