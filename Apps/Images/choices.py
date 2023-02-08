from django.db.models import TextChoices


class ImageTypeChoices(TextChoices):
    PC: str = "PC"
    TABLET: str = "TABLET"
    MOBILE: str = "MOBILE"
    OTHER: str = "OTHER"
