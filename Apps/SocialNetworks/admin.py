from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Model

from SocialNetworks.models import SocialNetwork


class SocialNetworkAdmin(ModelAdmin):
    model: Model = SocialNetwork
    list_display: tuple = ("id", "social_network_platform")
    list_display_links: tuple = ("id", "social_network_platform")
    list_filter: tuple = ("social_network_platform",)
    fieldsets: tuple = (
        ("Overview", {"fields": ("id", "social_network_platform", "nickname", "url")}),
    )
    readonly_fields: list = [
        "id",
    ]
    search_fields: tuple = ("url", "nickname", "social_network_platform", "id")


admin.site.register(SocialNetwork, SocialNetworkAdmin)
