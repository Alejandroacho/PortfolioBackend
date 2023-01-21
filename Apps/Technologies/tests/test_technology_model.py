import pytest

from Technologies.factories import TechnologyFactory
from Technologies.fakers import TechnologyFaker
from Technologies.models import Technology


@pytest.mark.django_db
class TestTechnologyModel:
    def test_model_keys(self) -> None:
        technology: Technology = TechnologyFaker()
        assert hasattr(technology, "id")
        assert hasattr(technology, "name")

    def test_str_representation(self) -> None:
        technology: Technology = TechnologyFaker()
        assert str(technology) == f"{technology.id} | {technology.name}"


@pytest.mark.django_db
class TestTechnologyFactory:
    def test_factory_creates_an_instance(self) -> None:
        assert Technology.objects.count() == 0
        technology: Technology = TechnologyFactory(name="Python")
        assert isinstance(technology, Technology)
        assert Technology.objects.count() == 1


@pytest.mark.django_db
class TestTechnologyFaker:
    def test_faker_create_the_default_python_instance(self) -> None:
        assert Technology.objects.count() == 0
        technology: Technology = TechnologyFaker()
        assert isinstance(technology, Technology)
        assert Technology.objects.count() == 1
        assert technology.name == "Python"
