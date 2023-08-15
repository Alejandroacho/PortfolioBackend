import os

from django.utils.html import format_html

from Project.settings.labels_with_svg import log_label_with_icon
from Project.settings.labels_with_svg import redoc_label_with_icon
from Project.settings.labels_with_svg import swagger_label_with_icon
from Project.settings.labels_with_svg import user_label_with_icon
from Project.utils.services_urls import set_services_urls


"""
JET Documentation: https://django-jet-reboot.readthedocs.io/
"""

set_services_urls()

X_FRAME_OPTIONS = "ALLOWALL"


JET_SIDE_MENU_COMPACT: bool = True


JET_THEMES: list = [
    {
        "theme": "default",  # theme folder name
        "color": "#47bac1",  # color of the theme's button in user menu
        "title": "Default",  # theme title
    },
    {"theme": "green", "color": "#44b78b", "title": "Green"},
    {"theme": "light-green", "color": "#2faa60", "title": "Light Green"},
    {"theme": "light-violet", "color": "#a464c4", "title": "Light Violet"},
    {"theme": "light-blue", "color": "#5EADDE", "title": "Light Blue"},
    {"theme": "light-gray", "color": "#222", "title": "Light Gray"},
]


JET_SIDE_MENU_ITEMS: list = [
    {
        "label": ("People"),
        "app_label": "Users",
        "items": [
            {"name": "user", "label": format_html(user_label_with_icon)},
        ],
    },
    {
        "label": "Portfolio",
        "items": [
            {
                "label": "Projects",
                "url": "/admin/Projects/project/",
                "url_blank": False,
            },
            {
                "label": "Experiences",
                "url": "/admin/Experiences/experience/",
                "url_blank": False,
            },
            {
                "label": "Certifications",
                "url": "/admin/Certifications/certification/",
                "url_blank": False,
            },
            {
                "label": "Technologies",
                "url": "/admin/Technologies/technology/",
                "url_blank": False,
            },
            {
                "label": "Authors",
                "url": "/admin/Authors/author/",
                "url_blank": False,
            },
            {
                "label": "SocialNetworks",
                "url": "/admin/SocialNetworks/socialnetwork/",
                "url_blank": False,
            },
            {
                "label": "Images",
                "url": "/admin/Images/image/",
                "url_blank": False,
            },
        ],
    },
    {
        "label": ("Administration"),
        "app_label": "admin",
        "items": [
            {"name": "logentry", "label": format_html(log_label_with_icon)}
        ],
    },
    {
        "label": "Documentation",
        "items": [
            {
                "label": format_html(swagger_label_with_icon),
                "url": "/docs/swagger/",
                "url_blank": True,
            },
            {
                "label": format_html(redoc_label_with_icon),
                "url": "/docs/redoc/",
                "url_blank": True,
            },
        ],
    },
    {
        "label": ("Others"),
        "items": [
            {
                "label": "Grafana",
                "url": f"http://{os.environ['GRAFANA_URL']}"
                if os.environ.setdefault("ENV", "local") == "local"
                else f"https://{os.environ['GRAFANA_URL']}",
                "url_blank": True,
            },
            {
                "label": "Prometheus",
                "url": f"http://{os.environ['PROMETHEUS_URL']}"
                if os.environ.setdefault("ENV", "local") == "local"
                else f"https://{os.environ['PROMETHEUS_URL']}",
                "url_blank": True,
            },
            {
                "label": "Flower",
                "url": f"http://{os.environ['FLOWER_URL']}"
                if os.environ.setdefault("ENV", "local") == "local"
                else f"https://{os.environ['FLOWER_URL']}",
                "url_blank": True,
            },
        ],
    },
]
