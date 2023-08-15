from django.db.models import TextChoices


class ImageTypeChoices(TextChoices):
    CARD: str = "CARD"
    OTHER: str = "OTHER"
