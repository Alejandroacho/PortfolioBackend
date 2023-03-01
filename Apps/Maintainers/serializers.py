from django.db.models import Model
from drf_extra_fields.fields import Base64FileField
from filetype import guess as guess_file_extension
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ModelSerializer

from Authors.models import Author
from Authors.serializers import AuthorSerializer
from Certifications.models import Certification
from Certifications.serializers import CertificationSerializer
from Images.models import Image
from Images.serializers import ImageSerializer
from Maintainers.models import Maintainer
from SocialNetworks.models import SocialNetwork
from SocialNetworks.serializers import SocialNetworkSerializer


class CustomFileField(Base64FileField):
    ALLOWED_TYPES: list = [
        "pdf",
    ]

    def get_file_extension(self, _, decoded_file) -> str:
        return guess_file_extension(decoded_file).extension


class MaintainerSerializer(ModelSerializer):
    cv = CustomFileField(required=False, allow_null=True)
    social_networks = SocialNetworkSerializer(many=True)
    certifications = CertificationSerializer(many=True)
    images = ImageSerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model: Model = Maintainer
        fields: str = "__all__"
        read_only_fields: list = ["id"]
        allow_empty_fields: list = [
            "social_networks",
            "certifications",
            "images",
            "cv",
        ]

    def to_representation(self, instance: Maintainer) -> dict:
        return {
            "id": instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "about": instance.about,
            "cv": instance.cv.url if instance.cv else None,
            "certifications": CertificationSerializer(
                instance.certifications.all(), many=True
            ).data,
            "images": ImageSerializer(instance.images.all(), many=True).data,
            "social_networks": SocialNetworkSerializer(
                instance.social_networks.all(), many=True
            ).data,
            "author": AuthorSerializer(instance.author).data,
        }

    def to_internal_value(self, data: dict) -> dict:
        return {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "about": data.get("about"),
            "cv": CustomFileField().to_internal_value(data.get("cv", None)),
            "certifications": Certification.objects.filter(
                id__in=data.pop("certifications", [])
            ),
            "images": Image.objects.filter(id__in=data.pop("images", [])),
            "social_networks": SocialNetwork.objects.filter(
                id__in=data.pop("social_networks", [])
            ),
            "author": Author.objects.filter(
                id=data.pop("author", None)
            ).first(),
        }

    def create(self, validated_data: dict) -> Maintainer:
        certifications = validated_data.pop("certifications")
        images = validated_data.pop("images")
        social_networks = validated_data.pop("social_networks")
        try:
            maintainer = Maintainer.objects.create(**validated_data)
        except ValueError as error:
            raise PermissionDenied(error)
        maintainer.certifications.set(certifications)
        maintainer.images.set(images)
        maintainer.social_networks.set(social_networks)
        return maintainer

    def update(self, instance: Maintainer, validated_data: dict) -> Maintainer:
        certifications = validated_data.pop("certifications")
        images = validated_data.pop("images")
        social_networks = validated_data.pop("social_networks")
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value or getattr(instance, attribute))
        instance.social_networks.set(social_networks)
        instance.certifications.set(certifications)
        instance.images.set(images)
        instance.save()
        return instance
