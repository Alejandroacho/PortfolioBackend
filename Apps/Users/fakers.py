from factory import post_generation
from factory.django import FileField

from Authors.fakers import AuthorFaker
from Certifications.fakers import CertificationFaker
from Images.fakers import ImageFaker
from SocialNetworks.fakers import SocialNetworkFaker
from Users.factories import UserFactory


class UserFaker(UserFactory):
    first_name: str = "Test"
    last_name: str = "Test"
    email: str = "test@appname.com"
    about: str = "Test description"
    cv: FileField = FileField(filename="cv.pdf")

    @post_generation
    def certifications(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for certification in extracted:
                self.certifications.add(certification)
        if not extracted:
            self.certifications.add(
                CertificationFaker().id, CertificationFaker().id
            )

    @post_generation
    def images(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for image in extracted:
                self.images.add(image)
        if not extracted:
            self.images.add(ImageFaker().id, ImageFaker().id)

    @post_generation
    def social_networks(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for social_network in extracted:
                self.social_networks.add(social_network)
        if not extracted:
            self.social_networks.add(
                SocialNetworkFaker().id, SocialNetworkFaker().id
            )

    @post_generation
    def author(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.author = extracted
        if not extracted:
            self.author = AuthorFaker()
