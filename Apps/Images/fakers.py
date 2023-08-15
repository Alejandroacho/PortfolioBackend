from django.db.models import CharField
from django.db.models import ImageField
from factory.django import ImageField

from Images.choices import ImageTypeChoices
from Images.factories import ImageFactory


class ImageFaker(ImageFactory):
    type: CharField = ImageTypeChoices.OTHER.value
    description: CharField = "This is a test image"
    image: ImageField = ImageField(
        filename="image.jpeg",
        width=100,
        height=100,
        format="JPEG",
        color="gray",
    )
