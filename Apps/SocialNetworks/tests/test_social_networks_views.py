import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from SocialNetworks.fakers import SocialNetworkFaker
from SocialNetworks.models import SocialNetwork
from Users.fakers import UserFaker
from Users.models import User


@pytest.mark.django_db
class TestRetrieveEndpoint:
    @staticmethod
    def url(social_network_id: int = None) -> str:
        return (
            reverse(
                "social-networks:social-networks-detail",
                kwargs={"pk": social_network_id},
            )
            if social_network_id
            else reverse("social-networks:social-networks-list")
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/social-networks/1/"
        assert self.url() == "/api/social-networks/"

    def test_works_as_unauthenticated(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        social_network2: SocialNetwork = SocialNetworkFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[1]["id"] == social_network.id
        assert response.data[1]["nickname"] == social_network.nickname
        assert response.data[1]["url"] == social_network.url
        assert response.data[0]["id"] == social_network2.id
        assert response.data[0]["nickname"] == social_network2.nickname
        assert response.data[0]["url"] == social_network2.url

