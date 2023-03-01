import pytest

from Authors.factories import AuthorFactory
from Authors.fakers import AuthorFaker
from Authors.models import Author


@pytest.mark.django_db
class TestAuthorModel:
    def test_model_keys(self) -> None:
        author: Author = AuthorFaker()
        assert hasattr(author, "id")
        assert hasattr(author, "first_name")
        assert hasattr(author, "last_name")
        assert hasattr(author, "social_networks")

    def test_name_property(self) -> None:
        author: Author = AuthorFaker()
        assert author.name == f"{author.first_name} {author.last_name}"

    def test_str_representation(self) -> None:
        author: Author = AuthorFaker()
        assert str(author) == f"{author.id} | {author.name}"


@pytest.mark.django_db
class TestAuthorFactory:
    def test_factory_creates_an_instance(self) -> None:
        assert Author.objects.count() == 0
        author: Author = AuthorFactory(
            first_name="TEST",
            last_name="TEST",
        )
        assert isinstance(author, Author)
        assert Author.objects.count() == 1


@pytest.mark.django_db
class TestAuthorFaker:
    def test_faker_create_the_default_instance(self) -> None:
        assert Author.objects.count() == 0
        author: Author = AuthorFaker()
        assert isinstance(author, Author)
        assert Author.objects.count() == 1
        assert author.first_name == "Fake Name"
        assert author.last_name == "Fake Last Name"
        assert author.social_networks.count() == 1
