from django.db.models import Model
from drf_extra_fields.fields import Base64FileField
from filetype import guess as guess_file_extension
from rest_framework.serializers import ModelSerializer

from Authors.serializers import AuthorSerializer
from Images.serializers import ImageSerializer
from Users.models import User


class CustomFileField(Base64FileField):
    ALLOWED_TYPES: list = [
        "pdf",
    ]

    def get_file_extension(self, _, decoded_file) -> str:
        return guess_file_extension(decoded_file).extension


class UserSerializer(ModelSerializer):
    cv = CustomFileField(required=False, allow_null=True)
    image = ImageSerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model: Model = User
        fields: str = "__all__"
        read_only_fields: list = ["id"]
        allow_empty_fields: list = [
            "image",
            "cv",
        ]

    def to_representation(self, instance: User) -> dict:
        return {
            "id": instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "about": instance.about,
            "cv": instance.cv.url if instance.cv else None,
            "image": ImageSerializer(instance.image).data,
            "author": AuthorSerializer(instance.author).data,
        }
