import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from Technologies.fakers import TechnologyFaker
from Technologies.models import Technology
from Users.fakers import UserFaker
from Users.models import User


@pytest.mark.django_db
class TestRetrieveEndpoint:
    @staticmethod
    def url(technology_id: int = None) -> str:
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

    def test_works_as_unauthenticated(self) -> None:
        technology: Technology = TechnologyFaker()
        technology2: Technology = TechnologyFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[1]["id"] == technology.id
        assert response.data[1]["name"] == technology.name
        assert response.data[0]["id"] == technology2.id
        assert response.data[0]["name"] == technology2.name
