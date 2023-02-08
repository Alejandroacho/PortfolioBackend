from django.db.models import CharField
from django.db.models import Model
from django.db.models.fields import Field

from SocialNetworks.choices import SocialNetworks


class SocialNetwork(Model):
    platform: Field = CharField(
        max_length=100,
        null=False,
        choices=SocialNetworks.choices,
    )
    nickname: Field = CharField(max_length=100, null=False)
    url: Field = CharField(max_length=100, null=False)

    def __str__(self) -> str:
        return f"{self.id} | {self.nickname} - {self.platform}"
