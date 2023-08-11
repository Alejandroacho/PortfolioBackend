from django.conf import settings
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django_rest_passwordreset.models import ResetPasswordToken

from Users.models import User


# Sets the admin logo
logo_url: str = "http://localhost:8000/static/logo.png"
admin.site.site_header = format_html(
    "<img src={url} height=50 width=50>", url=logo_url
)


# Sets the admin 'view site' url
site_url: str = settings.FRONTEND_URL
admin.site.site_url = site_url


# Sets the global admin titles
admin.site.site_title = settings.APP_NAME
admin.site.index_title = "Home"


# remove these lines if you want these models on admin
admin.site.unregister(Group)
admin.site.unregister(ResetPasswordToken)


class UserAdmin(BaseUserAdmin):
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
                    "image",
                    "author",
                )
            },
        ),
    )
    ordering: list = ("id",)
    readonly_fields: list = ["id"]
    search_fields: tuple = ("email", "last_name", "first_name", "id")


class LogEntryAdmin(ModelAdmin):
    list_display: tuple = (
        "user",
        "action_flag",
        "change_message",
    )
    search_fields: tuple = ("user__email",)
    date_hierarchy: str = "action_time"
    list_filter: tuple = ("action_flag", "content_type__model")
    list_per_page: int = 20


admin.site.register(User, UserAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
