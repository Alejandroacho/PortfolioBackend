from django.db.models import Model
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer

from Images.models import Image


class ImageSerializer(ModelSerializer):

    image: Base64ImageField = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model: Model = Image
        fields: str = "__all__"
        read_only_fields: list = ["id"]
