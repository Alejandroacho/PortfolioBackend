from django.urls import reverse
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Certifications.fakers import CertificationFaker
from Certifications.models import Certification


@mark.django_db
class TestRetrieveEndpoint:
    @staticmethod
    def url() -> str:
        return reverse("certifications:certifications-list")

    def test_url(self) -> None:
        assert self.url() == "/api/certifications/"

    def test_list_works(self) -> None:
        certification: Certification = CertificationFaker()
        certification2: Certification = CertificationFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[0]["id"] == certification2.id
        assert response.data[0]["name"] == certification2.name
        assert response.data[0]["description"] == certification2.description
        assert response.data[0]["tags"] == f"{certification2.tags}"
        assert response.data[0]["url"] == certification2.url
        assert certification2.image.url == response.data[0]["image"]["url"]
        assert certification2.file.url in response.data[0]["file"]
        assert response.data[1]["id"] == certification.id
        assert response.data[1]["name"] == certification.name
        assert response.data[1]["description"] == certification.description
        assert response.data[1]["tags"] == f"{certification.tags}"
        assert response.data[1]["url"] == certification.url
        assert certification.image.url == response.data[1]["image"]["url"]
        assert certification.file.url in response.data[1]["file"]
