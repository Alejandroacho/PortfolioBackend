from django.urls import reverse
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Authors.fakers import AuthorFaker
from Authors.models import Author
from SocialNetworks.fakers import SocialNetworkFaker
from SocialNetworks.serializers import SocialNetworkSerializer
from Users.fakers.user import UserFaker
from Users.models import User


@mark.django_db
class TestRetrieveEndpoint:
    def url(self, author_id: int = None) -> str:
        return (
            reverse(
                "authors:authors-detail",
                kwargs={"pk": author_id},
            )
            if author_id
            else reverse("authors:authors-list")
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/authors/1/"
        assert self.url() == "/api/authors/"

    def test_fails_as_unauthenticated(self) -> None:
        author: Author = AuthorFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url(author.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        author: Author = AuthorFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(author.id))
        assert response.status_code == 403

    def test_retrieve_works_as_admin(self) -> None:
        author: Author = AuthorFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(author.id))
        assert response.status_code == 200
        assert response.data["id"] == author.id
        assert response.data["first_name"] == author.first_name
        assert response.data["last_name"] == author.last_name
        assert (
            response.data["social_networks"]
            == SocialNetworkSerializer(author.social_networks, many=True).data
        )

    def test_list_works_as_admin(self) -> None:
        author: Author = AuthorFaker()
        author2: Author = AuthorFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[1]["id"] == author.id
        assert response.data[1]["first_name"] == author.first_name
        assert response.data[1]["last_name"] == author.last_name
        assert (
            response.data[1]["social_networks"]
            == SocialNetworkSerializer(author.social_networks, many=True).data
        )
        assert response.data[0]["id"] == author2.id
        assert response.data[0]["first_name"] == author2.first_name
        assert response.data[0]["last_name"] == author2.last_name
        assert (
            response.data[0]["social_networks"]
            == SocialNetworkSerializer(author2.social_networks, many=True).data
        )
