import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from Technologies.fakers import TechnologyFaker
from Technologies.models import Technology
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


@pytest.mark.django_db
class TestCreateEndpoint:
    def url(self) -> str:
        return reverse("technologies:technologies-list")

    def test_url(self) -> None:
        assert self.url() == "/api/technologies/"

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

    def test_works_as_admin(self) -> None:
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Technology.objects.count() == 0
        response: Response = client.post(self.url(), data={"name": "Kotlin"})
        assert response.status_code == 201
        assert Technology.objects.count() == 1
        assert Technology.objects.first().name == "Kotlin"


@pytest.mark.django_db
class TestRetrieveEndpoint:
    def url(self, technology_id: int = None) -> str:
        return (
            reverse(
                "technologies:technologies-detail", kwargs={"pk": technology_id}
            )
            if technology_id
            else reverse("technologies:technologies-list")
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/technologies/1/"
        assert self.url() == "/api/technologies/"

    def test_fails_as_unauthenticated(self) -> None:
        technology: Technology = TechnologyFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url(technology.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        technology: Technology = TechnologyFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(technology.id))
        assert response.status_code == 403

    def test_retrieve_works_as_admin(self) -> None:
        technology: Technology = TechnologyFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(technology.id))
        assert response.status_code == 200
        assert response.data["id"] == technology.id
        assert response.data["name"] == technology.name

    def test_list_works_as_admin(self) -> None:
        technology: Technology = TechnologyFaker()
        technology2: Technology = TechnologyFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[1]["id"] == technology.id
        assert response.data[1]["name"] == technology.name
        assert response.data[0]["id"] == technology2.id
        assert response.data[0]["name"] == technology2.name


@pytest.mark.django_db
class TestUpdateEndpoint:
    def url(self, technology_id: int) -> str:
        return reverse(
            "technologies:technologies-detail", kwargs={"pk": technology_id}
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/technologies/1/"

    def test_fails_as_unauthenticated(self) -> None:
        technology: Technology = TechnologyFaker()
        client: APIClient = APIClient()
        response: Response = client.put(self.url(technology.id), data={})
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        technology: Technology = TechnologyFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.put(self.url(technology.id), data={})
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        technology: Technology = TechnologyFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Technology.objects.count() == 1
        assert Technology.objects.first().name == "Python"
        response: Response = client.put(
            self.url(technology.id), data={"name": "Kotlin"}
        )
        assert response.status_code == 200
        assert Technology.objects.count() == 1
        assert Technology.objects.first().name == "Kotlin"


@pytest.mark.django_db
class TestDeleteEndpoint:
    def url(self, technology_id: int) -> str:
        return reverse(
            "technologies:technologies-detail", kwargs={"pk": technology_id}
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/technologies/1/"

    def test_fails_as_unauthenticated(self) -> None:
        technology: Technology = TechnologyFaker()
        client: APIClient = APIClient()
        response: Response = client.delete(self.url(technology.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        technology: Technology = TechnologyFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.delete(self.url(technology.id))
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        technology: Technology = TechnologyFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Technology.objects.count() == 1
        response: Response = client.delete(self.url(technology.id))
        assert response.status_code == 204
        assert Technology.objects.count() == 0
