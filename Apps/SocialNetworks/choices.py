from django.db.models import TextChoices


class SocialNetworks(TextChoices):
    LINKEDIN: str = "LINKEDIN"
    GITHUB: str = "GITHUB"
    INSTAGRAM: str = "INSTAGRAM"
    FACEBOOK: str = "FACEBOOK"
    TWITTER: str = "TWITTER"
    TIKTOK: str = "TIKTOK"
