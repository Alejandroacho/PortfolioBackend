from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Model

from SocialNetworks.models import SocialNetwork


class SocialNetworkAdmin(ModelAdmin):
    model: Model = SocialNetwork
    list_display: tuple = ("id", "nickname", "platform")
    list_display_links: tuple = ("id", "nickname")
    list_filter: tuple = ("platform",)
    fieldsets: tuple = (
        (
            "Overview",
            {"fields": ("id", "platform", "nickname", "url")},
        ),
    )
    readonly_fields: list = [
        "id",
    ]
    search_fields: tuple = ("url", "nickname", "platform", "id")


admin.site.register(SocialNetwork, SocialNetworkAdmin)
