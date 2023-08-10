from django.urls import reverse
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Images.fakers import ImageFaker
from Images.models import Image


@mark.django_db
class TestRetrieveEndpoint:
    @staticmethod
    def url(image_id: int = None) -> str:
        return (
            reverse("images:images-detail", kwargs={"pk": image_id})
            if image_id
            else reverse("images:images-list")
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/images/1/"
        assert self.url() == "/api/images/"

    def test_retrieve_works(self) -> None:
        image: Image = ImageFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url(image.id))
        assert response.status_code == 200
        assert response.data["id"] == image.id
        assert response.data["description"] == image.description
        assert response.data["type"] == image.type
        assert image.image.url in response.data["image"]

    def test_list_works(self) -> None:
        image: Image = ImageFaker()
        image2: Image = ImageFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[1]["id"] == image.id
        assert response.data[1]["description"] == image.description
        assert response.data[1]["type"] == image.type
        assert image.image.url in response.data[1]["image"]
        assert response.data[0]["id"] == image2.id
        assert response.data[0]["description"] == image2.description
        assert response.data[0]["type"] == image2.type
        assert image2.image.url in response.data[0]["image"]
