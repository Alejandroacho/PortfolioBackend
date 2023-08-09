from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Model

from Images.models import Image


class ImageAdmin(ModelAdmin):
    list_display: tuple = ("id", "description", "image_type")
    list_display_links: tuple = (
        "id",
        "description",
    )
    fieldsets: tuple = (
        ("Overview", {"fields": ("id", "image_type", "description", "image")}),
    )
    readonly_fields: list = [
        "id",
    ]
    search_fields: tuple = ("description", "image_type", "id")
    ordering: tuple = ("image_type",)


admin.site.register(Image, ImageAdmin)
