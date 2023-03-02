import base64
import os
from io import BufferedReader

from django.conf import settings
from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Certifications.fakers import CertificationFaker
from Certifications.models import Certification
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


@fixture(scope="class")
def base64_image() -> bytes:
    image_file: BufferedReader = open(f"{settings.STATIC_PATH}/logo.png", "rb")
    image_base64: bytes = base64.b64encode(image_file.read())
    image_file.close()
    return image_base64


@fixture(scope="class")
def base64_pdf_file() -> bytes:
    current_path: str = os.path.dirname(os.path.abspath(__file__))
    pdf_file: BufferedReader = open(f"{current_path}/test_file.pdf", "rb")
    pdf_base64: bytes = base64.b64encode(pdf_file.read())
    pdf_file.close()
    return pdf_base64


@mark.django_db
class TestCreateEndpoint:
    def url(self) -> str:
        return reverse("certifications:certifications-list")

    def test_url(self) -> None:
        assert self.url() == "/api/certifications/"

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

    def test_works_as_admin(
        self, base64_image: bytes, base64_pdf_file: bytes
    ) -> None:
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Certification.objects.count() == 0
        data: dict = {
            "name": "Certification name",
            "description": "Certification description",
            "url": "https://www.appname.me",
            "tags": "tag1,tag2,tag3",
            "image": base64_image,
            "file": base64_pdf_file,
        }
        response: Response = client.post(self.url(), data=data, format="json")
        assert response.status_code == 201
        assert Certification.objects.count() == 1
        assert Certification.objects.first().name == "Certification name"
        assert (
            Certification.objects.first().description
            == "Certification description"
        )
        assert Certification.objects.first().url == "https://www.appname.me"
        assert Certification.objects.first().tags == ["tag1", "tag2", "tag3"]
        assert "image_1" in Certification.objects.first().image.url
        assert "certification_1" in Certification.objects.first().file.url


@mark.django_db
class TestRetrieveEndpoint:
    def url(self, certification_id: int = None) -> str:
        return (
            reverse(
                "certifications:certifications-detail",
                kwargs={"pk": certification_id},
            )
            if certification_id
            else reverse("certifications:certifications-list")
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/certifications/1/"
        assert self.url() == "/api/certifications/"

    def test_fails_as_unauthenticated(self) -> None:
        certification: Certification = CertificationFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url(certification.id))
        assert response.status_code == 200

    def test_list_works_as_unauthenticated(self) -> None:
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
        assert certification2.image.url in response.data[0]["image"]
        assert certification2.file.url in response.data[0]["file"]
        assert response.data[1]["id"] == certification.id
        assert response.data[1]["name"] == certification.name
        assert response.data[1]["description"] == certification.description
        assert response.data[1]["tags"] == f"{certification.tags}"
        assert response.data[1]["url"] == certification.url
        assert certification.image.url in response.data[1]["image"]
        assert certification.file.url in response.data[1]["file"]

    def test_fails_as_unverified(self) -> None:
        certification: Certification = CertificationFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(certification.id))
        assert response.status_code == 200

    def test_retrieve_works_as_admin(self) -> None:
        certification: Certification = CertificationFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(certification.id))
        assert response.status_code == 200
        assert response.data["id"] == certification.id
        assert response.data["name"] == certification.name
        assert response.data["description"] == certification.description
        assert response.data["tags"] == f"{certification.tags}"
        assert response.data["url"] == certification.url
        assert certification.image.url in response.data["image"]
        assert certification.file.url in response.data["file"]

    def test_list_works_as_admin(self) -> None:
        certification: Certification = CertificationFaker()
        certification2: Certification = CertificationFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[0]["id"] == certification2.id
        assert response.data[0]["name"] == certification2.name
        assert response.data[0]["description"] == certification2.description
        assert response.data[0]["tags"] == f"{certification2.tags}"
        assert response.data[0]["url"] == certification2.url
        assert certification2.image.url in response.data[0]["image"]
        assert certification2.file.url in response.data[0]["file"]
        assert response.data[1]["id"] == certification.id
        assert response.data[1]["name"] == certification.name
        assert response.data[1]["description"] == certification.description
        assert response.data[1]["tags"] == f"{certification.tags}"
        assert response.data[1]["url"] == certification.url
        assert certification.image.url in response.data[1]["image"]
        assert certification.file.url in response.data[1]["file"]


@mark.django_db
class TestUpdateEndpoint:
    def url(self, certification_id: int) -> str:
        return reverse(
            "certifications:certifications-detail",
            kwargs={"pk": certification_id},
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/certifications/1/"

    def test_fails_as_unauthenticated(self) -> None:
        certification: Certification = CertificationFaker()
        client: APIClient = APIClient()
        response: Response = client.patch(self.url(certification.id), data={})
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        certification: Certification = CertificationFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.patch(self.url(certification.id), data={})
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        certification: Certification = CertificationFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Certification.objects.count() == 1
        assert (
            Certification.objects.first().description
            == "This is a fake certification"
        )
        response: Response = client.patch(
            self.url(certification.id),
            data={"description": "Kotlin certification"},
        )
        assert response.status_code == 200
        assert Certification.objects.count() == 1
        assert (
            Certification.objects.first().description == "Kotlin certification"
        )


@mark.django_db
class TestDeleteEndpoint:
    def url(self, certification_id: int) -> str:
        return reverse(
            "certifications:certifications-detail",
            kwargs={"pk": certification_id},
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/certifications/1/"

    def test_fails_as_unauthenticated(self) -> None:
        certification: Certification = CertificationFaker()
        client: APIClient = APIClient()
        response: Response = client.delete(self.url(certification.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        certification: Certification = CertificationFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.delete(self.url(certification.id))
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        certification: Certification = CertificationFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Certification.objects.count() == 1
        response: Response = client.delete(self.url(certification.id))
        assert response.status_code == 204
        assert Certification.objects.count() == 0
