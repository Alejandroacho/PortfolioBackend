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
