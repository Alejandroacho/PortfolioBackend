from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Model

from Technologies.models import Technology


class TechnologyAdmin(ModelAdmin):
    model: Model = Technology
    list_display: tuple = ("id", "name")
    list_display_links: tuple = ("id", "name")
    list_filter: tuple = ("name",)
    fieldsets: tuple = (("Overview", {"fields": ("id", "name")}),)
    readonly_fields: list = [
        "id",
    ]
    search_fields: tuple = ("name", "id")


admin.site.register(Technology, TechnologyAdmin)
