from django.db.models import Model
from drf_extra_fields.fields import Base64FileField
from filetype import guess as guess_file_extension
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ModelSerializer

from Authors.models import Author
from Authors.serializers import AuthorSerializer
from Images.models import Image
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

    def to_internal_value(self, data: dict) -> dict:
        return {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "about": data.get("about"),
            "cv": CustomFileField().to_internal_value(data.get("cv", None)),
            "image": Image.objects.filter(id__in=data.pop("image", [])),
            "author": Author.objects.filter(
                id=data.pop("author", None)
            ).first(),
        }

    def create(self, validated_data: dict) -> User:
        image = validated_data.pop("image")
        try:
            user = User.objects.create(**validated_data)
        except ValueError as error:
            raise PermissionDenied(error)
        user.image.set(image)
        return user

    def update(self, instance: User, validated_data: dict) -> User:
        image = validated_data.pop("image")
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value or getattr(instance, attribute))
        instance.image.set(image)
        instance.save()
        return instance
