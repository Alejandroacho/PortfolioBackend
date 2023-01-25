from django.db.models import CharField
from factory import SubFactory
from factory.django import FileField

from Certifications.factories import CertificationFactory
from Images.fakers import ImageFaker
from Images.models import Image


class CertificationFaker(CertificationFactory):
    name: CharField = "Fake"
    description: CharField = "This is a fake certification"
    tags: list = ["test", "test2", "test3"]
    url: CharField = "https://www.appname.com"
    image: Image = SubFactory(ImageFaker)
    file: FileField = FileField(
        filename="test.pdf",
        data=b"this is a test file",
    )
