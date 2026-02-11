from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

NAV_MENU = [
    {
        "heading": None,
        "items": [
            {
                "name": _("Admin"),
                "url": reverse_lazy("admin:index"),
                "icon": "fa-solid fa-screwdriver-wrench",
                "match_app": "admin",
            }
        ]
    }
]
