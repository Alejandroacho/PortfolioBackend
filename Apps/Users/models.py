from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import Field
from django.db.models import FileField
from django.db.models import ForeignKey
from django.db.models import Model
from django_prometheus.models import ExportModelOperationsMixin

from Authors.models import Author
from Certifications.models import Certification
from Images.models import Image
from SocialNetworks.models import SocialNetwork
from Users.manager import CustomUserManager


LIMIT: int = settings.MAINTAINERS_LIMIT


class User(
    ExportModelOperationsMixin("user"), AbstractBaseUser, PermissionsMixin
):
    username: None = None
    is_superuser: None = None
    last_login: None = None

    first_name: Field = CharField(max_length=100)
    last_name: Field = CharField(max_length=100)
    email: Field = CharField(
        max_length=100, unique=True, null=False, blank=False
    )
    about: Field = CharField(max_length=5000, null=False, blank=True)
    cv: Field = FileField(null=True, blank=True)
    image: Field = ForeignKey(
        Image,
        on_delete=CASCADE,
        related_name="images",
        blank=True,
        null=True,
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

    objects: BaseUserManager = CustomUserManager()

    def __str__(self) -> str:
        return str(self.email)

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self) -> bool:
        return True

    @staticmethod
    def has_permission(_: Model = None) -> bool:
        return True

    def has_perm(self, permission: str, _: Model = None) -> bool:
        return True

    def has_module_perms(self, _: str) -> bool:
        return True

    # There can only be a limited number of instances of this model in the DB
    def save(self, *args: tuple, **kwargs: dict) -> None:
        users_count: int = User.objects.count()
        users_ids: list = User.objects.values_list("pk", flat=True)
        if users_count == LIMIT and self.pk not in users_ids:
            raise ValueError(f"There can be only {LIMIT} user instance")
        return super().save(*args, **kwargs)
