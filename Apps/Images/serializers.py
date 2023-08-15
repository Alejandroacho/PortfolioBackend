from django.db.models import Model
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from Images.models import Image


class ImageSerializer(ModelSerializer):

    image: Base64ImageField = Base64ImageField(required=True, allow_null=False)
    url: str = CharField(source="image.url", read_only=True)

    class Meta:
        model: Model = Image
        fields: str = "__all__"
        read_only_fields: list = ["id"]
        exclude: list = ["image"]


class CustomImageField(Base64ImageField):
    def __init__(self, **kwargs) -> None:
        self.model = kwargs.pop("model", None)
        self.model_attribute = kwargs.pop("attribute", None)
        if not self.model or not self.model_attribute:
            raise ValueError("Model and attribute must be provided")
        super().__init__(**kwargs)

    def to_representation(self, instance: Image) -> str:
        return instance.image.url
