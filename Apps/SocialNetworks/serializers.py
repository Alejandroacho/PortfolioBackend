from django.db.models import Model
from rest_framework.serializers import ModelSerializer

from SocialNetworks.models import SocialNetwork


class SocialNetworkSerializer(ModelSerializer):
    class Meta:
        model: Model = SocialNetwork
        fields: str = "__all__"
        read_only_fields: list = ["id"]
