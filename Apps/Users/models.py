import datetime

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models import CASCADE, ManyToManyField, ForeignKey
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import Field
from django.db.models import FileField
from django.db.models import Model
from django_prometheus.models import ExportModelOperationsMixin

from Authors.models import Author
from Certifications.models import Certification
from Images.models import Image
from SocialNetworks.models import SocialNetwork

LIMIT: int = settings.MAINTAINERS_LIMIT


class User(
    ExportModelOperationsMixin("user"), AbstractBaseUser, PermissionsMixin
):
    username: None = None
    is_superuser: None = None
    last_login: None = None

    first_name: Field = CharField(max_length=100)
    last_name: Field = CharField(max_length=100)
    email: Field = CharField(max_length=100, unique=True, null=False, blank=False)
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

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list = ["first_name", "last_name"]

    def __str__(self) -> str:
        return str(self.email)

    # There can only be a limited number of instances of this model in the DB
    def save(self, *args: tuple, **kwargs: dict) -> None:
        maintainers_count: int = User.objects.count()
        maintainers_ids: list = User.objects.values_list("pk", flat=True)
        if maintainers_count == LIMIT and self.pk not in maintainers_ids:
            raise ValueError(f"There can be only {LIMIT} Maintainer instance")
        return super().save(*args, **kwargs)
