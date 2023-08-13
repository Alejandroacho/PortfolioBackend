from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Model

from Experiences.models import Experience


class ExperienceNetworkAdmin(ModelAdmin):
    model: Model = Experience
    list_display: tuple = ("id", "company", "time_of_experience")
    list_display_links: tuple = ("id", "company")
    list_filter: tuple = ("company", "position")
    fieldsets: tuple = (
        ("Overview", {"fields": ("id", "description")}),
        ("Job", {"fields": ("position", "technologies")}),
        ("Duration", {"fields": ("start_date", "end_date", "current")}),
        ("Company", {"fields": ("logo", "company", "url")}),
    )
    readonly_fields: list = [
        "id",
    ]
    search_fields: tuple = ("company", "position")


admin.site.register(Experience, ExperienceNetworkAdmin)
