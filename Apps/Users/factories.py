from django.db.models import Model
from factory import PostGenerationMethodCall
from factory import post_generation
from factory.django import DjangoModelFactory

from Users.models import User


class UserFactory(DjangoModelFactory):
    password: str = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model: Model = User

    @post_generation
    def images(self, create: bool, extracted: list, **kwargs: dict) -> None:
        if not create:
            return
        if extracted:
            for image in extracted:
                self.images.add(image)

    @post_generation
    def authors(self, create: bool, extracted: list, **kwargs: dict) -> None:
        if not create:
            return
        if extracted:
            for author in extracted:
                self.authors.add(author)

    @post_generation
    def social_networks(
        self, create: bool, extracted: list, **kwargs: dict
    ) -> None:
        if not create:
            return
        if extracted:
            for social_network in extracted:
                self.social_networks.add(social_network)

    @post_generation
    def certifications(
        self, create: bool, extracted: list, **kwargs: dict
    ) -> None:
        if not create:
            return
        if extracted:
            for certification in extracted:
                self.certifications.add(certification)
