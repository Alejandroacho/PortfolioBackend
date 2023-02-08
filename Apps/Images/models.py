from django.db.models import CharField
from django.db.models import ImageField
from django.db.models import Model
from django.db.models.fields import Field

from Images.choices import ImageTypeChoices
from Project.storage import get_image_storage
from Project.storage import image_file_upload


class Image(Model):
    type: Field = CharField(
        max_length=100,
        null=False,
        choices=ImageTypeChoices.choices,
    )
    description: Field = CharField(max_length=100, null=False)
    image: Field = ImageField(
        "Image",
        storage=get_image_storage(),
        upload_to=image_file_upload,
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.type} image"

    @property
    def url(self) -> str:
        return self.image.url

    @property
    def name(self) -> str:
        return self.image.name
