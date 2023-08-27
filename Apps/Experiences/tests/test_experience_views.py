from django.urls import reverse
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Experiences.fakers import ExperienceFaker
from Experiences.models import Experience


@mark.django_db
class TestRetrieveEndpoint:
    @staticmethod
    def url() -> str:
        return reverse("experiences:experiences-list")

    def test_url(self) -> None:
        assert self.url() == "/api/experiences/"

    def test_list_works(self) -> None:
        experience: Experience = ExperienceFaker()
        experience2: Experience = ExperienceFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[1]["id"] == experience.id
        assert response.data[1]["company"] == experience.company
        assert response.data[1]["description"] == experience.description
        assert response.data[1]["url"] == experience.url
        assert response.data[0]["id"] == experience2.id
        assert response.data[0]["company"] == experience2.company
        assert response.data[0]["description"] == experience2.description
        assert response.data[0]["url"] == experience2.url
