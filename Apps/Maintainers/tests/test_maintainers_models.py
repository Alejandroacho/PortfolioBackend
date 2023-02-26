import pytest

from Maintainers.factories import MaintainerFactory
from Maintainers.fakers import MaintainerFaker
from Maintainers.models import Maintainer


@pytest.mark.django_db
class TestMaintainerModel:
    def test_model_keys(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        assert hasattr(maintainer, "id")
        assert hasattr(maintainer, "first_name")
        assert hasattr(maintainer, "last_name")
        assert hasattr(maintainer, "email")
        assert hasattr(maintainer, "about")
        assert hasattr(maintainer, "cv")
        assert hasattr(maintainer, "certifications")
        assert hasattr(maintainer, "images")
        assert hasattr(maintainer, "social_networks")
        assert hasattr(maintainer, "author")

    def test_str_representation(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        assert str(maintainer) == f"{maintainer.id} | {maintainer.first_name}"


@pytest.mark.django_db
class TestMaintainerFactory:
    def test_factory_creates_an_instance(self) -> None:
        assert Maintainer.objects.count() == 0
        maintainer: Maintainer = MaintainerFactory(
            first_name="Test", last_name="Test", email="test@appname.com"
        )
        assert isinstance(maintainer, Maintainer)
        assert Maintainer.objects.count() == 1


@pytest.mark.django_db
class TestMaintainerFaker:
    def test_faker_create_the_default_python_instance(self) -> None:
        assert Maintainer.objects.count() == 0
        maintainer: Maintainer = MaintainerFaker()
        assert isinstance(maintainer, Maintainer)
        assert Maintainer.objects.count() == 1
        assert maintainer.first_name == "Test"
        assert maintainer.last_name == "Test"
        assert maintainer.email == "test@appname.com"
        assert maintainer.about == "Test description"
        assert "cv" in maintainer.cv.name
        assert "pdf" in maintainer.cv.name
        assert maintainer.certifications.count() == 2
        assert maintainer.images.count() == 2
        assert maintainer.social_networks.count() == 2
        assert maintainer.author is not None
