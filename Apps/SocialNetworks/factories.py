from django.db.models import Model
from factory.django import DjangoModelFactory

from SocialNetworks.models import SocialNetwork


class SocialNetworkFactory(DjangoModelFactory):
    class Meta:
        model: Model = SocialNetwork
