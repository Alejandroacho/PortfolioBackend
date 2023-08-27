import pytest
from django.db.models.fields.files import ImageFieldFile

from Images.factories import ImageFactory
from Images.fakers import ImageFaker
from Images.models import Image


@pytest.mark.django_db
class TestImageModel:
    def test_model_keys(self) -> None:
        image: Image = ImageFaker()
        assert hasattr(image, "id")
        assert hasattr(image, "type")
        assert hasattr(image, "description")
        assert hasattr(image, "image")

    def test_str_representation(self) -> None:
        image: Image = ImageFaker()
        assert str(image) == f"{image.id} | {image.description}"


@pytest.mark.django_db
class TestImageFactory:
    def test_factory_creates_an_instance(self) -> None:
        assert Image.objects.count() == 0
        image: Image = ImageFactory(
            type="OTHER",
            description="This is a test image",
            image="image.jpeg",
        )
        assert isinstance(image, Image)
        assert Image.objects.count() == 1


@pytest.mark.django_db
class TestImageFaker:
    def test_faker_create_the_default_python_instance(self) -> None:
        assert Image.objects.count() == 0
        image: Image = ImageFaker()
        assert isinstance(image, Image)
        assert Image.objects.count() == 1
        assert image.type == "OTHER"
        assert image.description == "This is a test image"
        assert isinstance(image.image, ImageFieldFile)
