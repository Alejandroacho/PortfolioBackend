from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Model
from drf_extra_fields.fields import Base64ImageField
from factory.django import DjangoModelFactory
from rest_framework.serializers import ModelSerializer

from Images import factories
from Images.models import Image


class ImageSerializer(ModelSerializer):

    image: Base64ImageField = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model: Model = Image
        fields: str = "__all__"
        read_only_fields: list = ["id"]


class CustomImageField(Base64ImageField):
    def __init__(self, **kwargs) -> None:
        self.model = kwargs.pop("model", None)
        self.model_attribute = kwargs.pop("attribute", None)
        if not self.model or not self.model_attribute:
            raise ValueError("Model and attribute must be provided")
        super().__init__(**kwargs)

    def get_factory(self) -> DjangoModelFactory:
        if self.model == "Image":
            return getattr(factories, f"ImageFactory")
        factory_name: str = f"{self.model}{self.model_attribute}Factory"
        if not hasattr(factories, factory_name):
            raise ValueError(f"Factory {factory_name} not found")
        return getattr(factories, factory_name)

    def to_internal_value(self, data: str) -> Image:
        if data:
            image: SimpleUploadedFile = super().to_internal_value(data)
            factory: DjangoModelFactory = self.get_factory()
            description: str = f"{self.model} {self.model_attribute}"
            data = factory.create(image=image, description=description)
        return data

    def to_representation(self, instance: Image) -> str:
        return instance.image.url
