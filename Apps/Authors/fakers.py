from django.db.models import Model
from factory import post_generation

from Authors.factories import AuthorFactory
from SocialNetworks.fakers import SocialNetworkFaker


class AuthorFaker(AuthorFactory):
    first_name: str = "Fake Name"
    last_name: str = "Fake Last Name"

    @post_generation
    def social_networks(
        self, create: bool, extracted: Model, **kwargs: dict
    ) -> None:
        self.social_networks.add(SocialNetworkFaker())
