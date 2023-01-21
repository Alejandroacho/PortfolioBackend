from django.db.models import Model
from factory.django import DjangoModelFactory

from Images.models import Image


class ImageFactory(DjangoModelFactory):
    class Meta:
        model: Model = Image
