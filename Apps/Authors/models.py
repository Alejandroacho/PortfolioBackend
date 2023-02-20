from django.db.models import CharField
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models.fields import Field

from SocialNetworks.models import SocialNetwork


class Author(Model):
    first_name: Field = CharField(max_length=100, null=True)
    last_name: Field = CharField(max_length=100, null=True)
    social_networks: Field = ManyToManyField(
        SocialNetwork, related_name="authors", null=True
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.first_name} {self.last_name}"

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
