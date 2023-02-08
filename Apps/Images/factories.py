from django.db.models import Model
from factory.django import DjangoModelFactory

from Images.choices import ImageTypeChoices
from Images.models import Image


class ImageFactory(DjangoModelFactory):
    class Meta:
        model: Model = Image


class CertificationImageFactory(ImageFactory):
    type: str = ImageTypeChoices.OTHER.name
    description: str = "Certification image"
