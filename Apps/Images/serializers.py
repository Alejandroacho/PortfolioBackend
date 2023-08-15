from django.db.models import Model
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from Images.models import Image


class ImageSerializer(ModelSerializer):
    url: str = CharField(source="image.url", read_only=True)

    class Meta:
        model: Model = Image
        fields: list = ["id", "type", "url", "description"]
        read_only_fields: list = ["id"]
