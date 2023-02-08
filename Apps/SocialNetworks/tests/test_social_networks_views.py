import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from SocialNetworks.fakers import SocialNetworkFaker
from SocialNetworks.models import SocialNetwork
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


@pytest.mark.django_db
class TestCreateEndpoint:
    def url(self) -> str:
        return reverse("social-networks:social-networks-list")

    def test_url(self) -> None:
        assert self.url() == "/api/social-networks/"

    def test_fails_as_unauthenticated(self) -> None:
        client: APIClient = APIClient()
        response: Response = client.post(self.url(), data={})
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.post(self.url(), data={})
        assert response.status_code == 403

    def test_fails_with_non_accepted_platform(self) -> None:
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.post(
            self.url(),
            data={
                "platform": "NON_EXISTENT",
                "nickname": "User",
                "url": "https://www.blabla.com/user/",
            },
        )
        assert response.status_code == 400
        assert '"NON_EXISTENT" is not a valid choice.' in str(
            response.data["platform"][0]
        )

    def test_works_as_admin(self) -> None:
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert SocialNetwork.objects.count() == 0
        response: Response = client.post(
            self.url(),
            data={
                "platform": "LINKEDIN",
                "nickname": "User",
                "url": "https://www.linkedin.com/in/user/",
            },
        )
        assert response.status_code == 201
        assert SocialNetwork.objects.count() == 1
        assert SocialNetwork.objects.first().nickname == "User"
        assert (
            SocialNetwork.objects.first().url
            == "https://www.linkedin.com/in/user/"
        )
        assert SocialNetwork.objects.first().platform == "LINKEDIN"


@pytest.mark.django_db
class TestRetrieveEndpoint:
    def url(self, social_network_id: int = None) -> str:
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

    def test_fails_as_unauthenticated(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url(social_network.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(social_network.id))
        assert response.status_code == 403

    def test_retrieve_works_as_admin(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(social_network.id))
        assert response.status_code == 200
        assert response.data["id"] == social_network.id
        assert response.data["nickname"] == social_network.nickname
        assert response.data["url"] == social_network.url

    def test_list_works_as_admin(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        social_network2: SocialNetwork = SocialNetworkFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[1]["id"] == social_network.id
        assert response.data[1]["nickname"] == social_network.nickname
        assert response.data[1]["url"] == social_network.url
        assert response.data[0]["id"] == social_network2.id
        assert response.data[0]["nickname"] == social_network2.nickname
        assert response.data[0]["url"] == social_network2.url


@pytest.mark.django_db
class TestUpdateEndpoint:
    def url(self, social_network_id: int) -> str:
        return reverse(
            "social-networks:social-networks-detail",
            kwargs={"pk": social_network_id},
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/social-networks/1/"

    def test_fails_as_unauthenticated(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        client: APIClient = APIClient()
        response: Response = client.put(self.url(social_network.id), data={})
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.put(self.url(social_network.id), data={})
        assert response.status_code == 403

    def test_fails_with_non_accepted_platform(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.patch(
            self.url(social_network.id),
            data={
                "platform": "NON_EXISTENT",
                "nickname": "User",
                "url": "https://www.blabla.com/user/",
            },
        )
        assert response.status_code == 400
        assert '"NON_EXISTENT" is not a valid choice.' in str(
            response.data["platform"][0]
        )

    def test_works_as_admin(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert SocialNetwork.objects.count() == 1
        assert SocialNetwork.objects.first().platform == "LINKEDIN"
        assert SocialNetwork.objects.first().nickname == "Username"
        response: Response = client.patch(
            self.url(social_network.id),
            data={"platform": "TIKTOK", "nickname": "Nickname"},
        )
        assert response.status_code == 200
        assert SocialNetwork.objects.count() == 1
        assert SocialNetwork.objects.first().platform == "TIKTOK"
        assert SocialNetwork.objects.first().nickname == "Nickname"


@pytest.mark.django_db
class TestDeleteEndpoint:
    def url(self, social_network_id: int) -> str:
        return reverse(
            "social-networks:social-networks-detail",
            kwargs={"pk": social_network_id},
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/social-networks/1/"

    def test_fails_as_unauthenticated(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        client: APIClient = APIClient()
        response: Response = client.delete(self.url(social_network.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.delete(self.url(social_network.id))
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert SocialNetwork.objects.count() == 1
        response: Response = client.delete(self.url(social_network.id))
        assert response.status_code == 204
        assert SocialNetwork.objects.count() == 0
