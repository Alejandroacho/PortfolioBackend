from factory import post_generation
from factory.django import FileField

from Authors.fakers import AuthorFaker
from Images.fakers import ImageFaker
from Users.factories import UserFactory


class UserFaker(UserFactory):
    first_name: str = "Test"
    last_name: str = "Test"
    email: str = "test@appname.com"
    about: str = "Test description"
    cv: FileField = FileField(filename="cv.pdf")

    @post_generation
    def image(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.image = extracted
        if not extracted:
            self.image = ImageFaker()

    @post_generation
    def author(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.author = extracted
        if not extracted:
            self.author = AuthorFaker()
