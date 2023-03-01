from django.db.models import Model
from rest_framework.serializers import ModelSerializer

from Authors.models import Author
from SocialNetworks.models import SocialNetwork
from SocialNetworks.serializers import SocialNetworkSerializer


class AuthorSerializer(ModelSerializer):
    social_networks = SocialNetworkSerializer(many=True)

    class Meta:
        model: Model = Author
        fields: str = "__all__"
        read_only_fields: list = ["id"]
        allow_empty_fields: list = ["social_networks"]

    def to_representation(self, instance: Author) -> dict:
        return {
            "id": instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "social_networks": SocialNetworkSerializer(
                instance.social_networks.all(), many=True
            ).data,
        }

    def to_internal_value(self, data: dict) -> dict:
        social_networks = data.pop("social_networks")
        return {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "social_networks": SocialNetwork.objects.filter(
                id__in=social_networks
            ),
        }

    def create(self, validated_data: dict) -> Author:
        social_networks = validated_data.pop("social_networks")
        author = Author.objects.create(**validated_data)
        author.social_networks.set(social_networks)
        return author

    def update(self, instance: Author, validated_data: dict) -> Author:
        social_networks = validated_data.pop("social_networks")
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value or getattr(instance, attribute))
        instance.social_networks.set(social_networks)
        instance.save()
        return instance
