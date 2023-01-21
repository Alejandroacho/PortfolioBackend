import base64
from io import BufferedReader

from django.conf import settings
from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Images.fakers import ImageFaker
from Images.models import Image
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


@fixture(scope="class")
def base64_image() -> bytes:
    image_file: BufferedReader = open(f"{settings.STATIC_PATH}/logo.png", "rb")
    image_base64: bytes = base64.b64encode(image_file.read())
    image_file.close()
    return image_base64


@mark.django_db
class TestCreateEndpoint:
    def url(self) -> str:
        return reverse("images:images-list")

    def test_url(self) -> None:
        assert self.url() == "/api/images/"

    def test_fails_as_unauthenticated(self) -> None:
        client: APIClient = APIClient()
        response: Response = client.post(self.url(), data={}, format="json")
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.post(self.url(), data={}, format="json")
        assert response.status_code == 403

    def test_works_as_admin(self, base64_image: bytes) -> None:
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Image.objects.count() == 0
        response: Response = client.post(
            self.url(),
            data={
                "type": "PC",
                "description": "Image description",
                "image": base64_image,
            },
            format="json",
        )
        assert response.status_code == 201
        assert Image.objects.count() == 1
        assert Image.objects.first().type == "PC"
        assert Image.objects.first().description == "Image description"
        assert "image_1" in Image.objects.first().image.url


@mark.django_db
class TestRetrieveEndpoint:
    def url(self, image_id: int = None) -> str:
        return (
            reverse("images:images-detail", kwargs={"pk": image_id})
            if image_id
            else reverse("images:images-list")
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/images/1/"
        assert self.url() == "/api/images/"

    def test_fails_as_unauthenticated(self) -> None:
        image: Image = ImageFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url(image.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        image: Image = ImageFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(image.id))
        assert response.status_code == 403

    def test_retrieve_works_as_admin(self) -> None:
        image: Image = ImageFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(image.id))
        assert response.status_code == 200
        assert response.data["id"] == image.id
        assert response.data["description"] == image.description
        assert response.data["type"] == image.type
        assert image.image.url in response.data["image"]

    def test_list_works_as_admin(self) -> None:
        image: Image = ImageFaker()
        image2: Image = ImageFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
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


@mark.django_db
class TestUpdateEndpoint:
    def url(self, image_id: int) -> str:
        return reverse("images:images-detail", kwargs={"pk": image_id})

    def test_url(self) -> None:
        assert self.url(1) == "/api/images/1/"

    def test_fails_as_unauthenticated(self) -> None:
        image: Image = ImageFaker()
        client: APIClient = APIClient()
        response: Response = client.patch(self.url(image.id), data={})
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        image: Image = ImageFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.patch(self.url(image.id), data={})
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        image: Image = ImageFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Image.objects.count() == 1
        assert Image.objects.first().type == "PC"
        assert Image.objects.first().description == "This is a test image"
        response: Response = client.patch(
            self.url(image.id), data={"description": "Kotlin project"}
        )
        assert response.status_code == 200
        assert Image.objects.count() == 1
        assert Image.objects.first().description == "Kotlin project"


@mark.django_db
class TestDeleteEndpoint:
    def url(self, image_id: int) -> str:
        return reverse("images:images-detail", kwargs={"pk": image_id})

    def test_url(self) -> None:
        assert self.url(1) == "/api/images/1/"

    def test_fails_as_unauthenticated(self) -> None:
        image: Image = ImageFaker()
        client: APIClient = APIClient()
        response: Response = client.delete(self.url(image.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        image: Image = ImageFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.delete(self.url(image.id))
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        image: Image = ImageFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Image.objects.count() == 1
        response: Response = client.delete(self.url(image.id))
        assert response.status_code == 204
        assert Image.objects.count() == 0
