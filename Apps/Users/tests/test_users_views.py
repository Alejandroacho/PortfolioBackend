from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Users.fakers import UserFaker
from Users.models import User


@fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@mark.django_db
class TestUserListEndpoint:
    @staticmethod
    def url() -> str:
        return reverse("users:users-list")

    def test_url(self) -> None:
        assert self.url() == "/api/users/"

    def test_list_users_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        response: Response = client.get(self.url(), format="json")
        assert response.status_code == 200


@mark.django_db
class TestUserRetrieveEndpoint:
    @staticmethod
    def url(pk: int = None) -> str:
        return reverse("users:users-detail", args=[pk])

    def test_url(self) -> None:
        assert self.url(1) == "/api/users/1/"

    def test_get_user_works_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        response: Response = client.get(self.url(normal_user.id), format="json")
        assert response.status_code == 200
