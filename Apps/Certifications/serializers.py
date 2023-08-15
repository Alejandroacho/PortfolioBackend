from django.db.models import Model
from drf_extra_fields.fields import Base64FileField
from filetype import guess as guess_file_extension
from rest_framework.fields import CharField
from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer

from Certifications.models import Certification
from Images.serializers import ImageSerializer


class CustomFileField(Base64FileField):
    ALLOWED_TYPES: list = [
        "pdf",
    ]

    def get_file_extension(self, _, decoded_file) -> str:
        return guess_file_extension(decoded_file).extension


class CertificationSerializer(ModelSerializer):
    name: Field = CharField(max_length=100, allow_null=True)
    description: Field = CharField(max_length=1000, allow_null=True)
    tags: Field = CharField(max_length=1000, allow_null=True)
    url: Field = CharField(max_length=1000, allow_null=True)
    file: Base64FileField = CustomFileField(required=False, allow_null=True)
    image: Field = ImageSerializer(
        required=False,
        allow_null=True,
    )

    class Meta:
        model: Model = Certification
        fields: str = "__all__"
        read_only_fields: list = ["id"]
