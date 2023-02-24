from django.conf import settings
from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import FileField
from django.db.models import ForeignKey
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models.fields import Field

from Authors.models import Author
from Certifications.models import Certification
from Images.models import Image
from SocialNetworks.models import SocialNetwork


LIMIT: int = settings.MAINTAINERS_LIMIT


class Maintainer(Model):
    first_name: Field = CharField(max_length=100)
    last_name: Field = CharField(max_length=100)
    email: Field = CharField(max_length=100)
    about: Field = CharField(max_length=5000, null=False, blank=True)
    cv: Field = FileField(null=True, blank=True)
    certifications: Field = ManyToManyField(
        Certification,
        related_name="certifications",
        blank=True,
    )
    images: Field = ManyToManyField(
        Image,
        related_name="images",
        blank=True,
    )
    social_networks: Field = ManyToManyField(
        SocialNetwork,
        related_name="social_networks",
        blank=True,
    )
    author: Field = ForeignKey(
        Author,
        on_delete=CASCADE,
        related_name="author",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.first_name}"

    ## There can only be a limited number of instances of this model in the DB
    def save(self, *args: tuple, **kwargs: dict) -> None:
        maintainers_count: int = Maintainer.objects.count()
        maintainers_ids: list = Maintainer.objects.values_list("pk", flat=True)
        if maintainers_count == LIMIT and not self.pk in maintainers_ids:
            raise ValueError(f"There can be only {LIMIT} Maintainer instance")
        return super().save(*args, **kwargs)
