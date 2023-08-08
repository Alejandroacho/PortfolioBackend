import base64
import os
from io import BufferedReader

from django.conf import settings
from django.urls import reverse
from pytest import fixture
from pytest import mark
from rest_framework.response import Response
from rest_framework.test import APIClient

from Authors.fakers import AuthorFaker
from Authors.serializers import AuthorSerializer
from Certifications.fakers import CertificationFaker
from Certifications.serializers import CertificationSerializer
from Images.fakers import ImageFaker
from Images.serializers import ImageSerializer
from Maintainers.fakers import MaintainerFaker
from Maintainers.models import Maintainer
from SocialNetworks.fakers import SocialNetworkFaker
from SocialNetworks.serializers import SocialNetworkSerializer
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


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
        return reverse("maintainers:maintainers-list")

    def test_url(self) -> None:
        assert self.url() == "/api/maintainers/"

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

    def test_works_as_admin_with_many_related_models(
        self, base64_pdf_file: str
    ) -> None:
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Maintainer.objects.count() == 0
        data: dict = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "email@appname.com",
            "about": "About",
            "cv": base64_pdf_file,
            "social_networks": [
                SocialNetworkFaker().id,
                SocialNetworkFaker().id,
            ],
            "certifications": [
                CertificationFaker().id,
                CertificationFaker().id,
            ],
            "images": [
                ImageFaker().id,
                ImageFaker().id,
            ],
            "author": AuthorFaker().id,
        }
        response: Response = client.post(self.url(), data=data, format="json")
        assert response.status_code == 201
        assert Maintainer.objects.count() == 1
        assert Maintainer.objects.first().first_name == "First name"
        assert Maintainer.objects.first().last_name == "Last name"
        assert Maintainer.objects.first().email == "email@appname.com"
        assert Maintainer.objects.first().about == "About"
        assert Maintainer.objects.first().cv is not None
        assert Maintainer.objects.first().social_networks.count() == 2
        assert Maintainer.objects.first().certifications.count() == 2
        assert Maintainer.objects.first().images.count() == 2
        assert Maintainer.objects.first().author is not None

    def test_works_as_admin_with_no_related_models(
        self, base64_pdf_file: str
    ) -> None:
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Maintainer.objects.count() == 0
        data: dict = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "email@appname.com",
            "about": "About",
            "cv": base64_pdf_file,
            "author": AuthorFaker().id,
        }
        response: Response = client.post(self.url(), data=data, format="json")
        assert response.status_code == 201
        assert Maintainer.objects.count() == 1
        assert Maintainer.objects.first().first_name == "First name"
        assert Maintainer.objects.first().last_name == "Last name"
        assert Maintainer.objects.first().email == "email@appname.com"
        assert Maintainer.objects.first().about == "About"
        assert Maintainer.objects.first().cv is not None
        assert Maintainer.objects.first().social_networks.count() == 0
        assert Maintainer.objects.first().certifications.count() == 0
        assert Maintainer.objects.first().images.count() == 0
        assert Maintainer.objects.first().author is not None

    def test_fails_if_the_maintainer_limit_is_reached(
        self, base64_pdf_file: str
    ) -> None:
        limit: int = settings.MAINTAINERS_LIMIT
        for _ in range(limit):
            MaintainerFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Maintainer.objects.count() == limit
        data: dict = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "test@appname.com",
            "about": "About",
            "cv": base64_pdf_file,
            "social_networks": [
                SocialNetworkFaker().id,
                SocialNetworkFaker().id,
            ],
            "certifications": [
                CertificationFaker().id,
                CertificationFaker().id,
            ],
            "images": [
                ImageFaker().id,
                ImageFaker().id,
            ],
            "author": AuthorFaker().id,
        }
        response: Response = client.post(self.url(), data=data, format="json")
        assert response.status_code == 403
        error_message: str = f"There can be only {limit} Maintainer instance"
        assert error_message in response.json()["detail"]


@mark.django_db
class TestRetrieveEndpoint:
    def url(self, maintainer_id: int = None) -> str:
        return (
            reverse(
                "maintainers:maintainers-detail",
                kwargs={"pk": maintainer_id},
            )
            if maintainer_id
            else reverse("maintainers:maintainers-list")
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/maintainers/1/"
        assert self.url() == "/api/maintainers/"

    def test_fails_as_unauthenticated(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url(maintainer.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(maintainer.id))
        assert response.status_code == 403

    def test_retrieve_works_as_admin(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(maintainer.id))
        assert response.status_code == 200
        assert response.data["id"] == maintainer.id
        assert response.data["first_name"] == maintainer.first_name
        assert response.data["last_name"] == maintainer.last_name
        assert response.data["email"] == maintainer.email
        assert response.data["about"] == maintainer.about
        assert response.data["cv"] == maintainer.cv.url
        assert (
            response.data["social_networks"]
            == SocialNetworkSerializer(
                maintainer.social_networks, many=True
            ).data
        )
        assert (
            response.data["certifications"]
            == CertificationSerializer(
                maintainer.certifications, many=True
            ).data
        )
        assert (
            response.data["images"]
            == ImageSerializer(maintainer.images, many=True).data
        )
        assert (
            response.data["author"] == AuthorSerializer(maintainer.author).data
        )


@mark.django_db
class TestUpdateEndpoint:
    def url(self, maintainer_id: int) -> str:
        return reverse(
            "maintainers:maintainers-detail",
            kwargs={"pk": maintainer_id},
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/maintainers/1/"

    def test_fails_as_unauthenticated(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        client: APIClient = APIClient()
        response: Response = client.patch(self.url(maintainer.id), data={})
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.patch(self.url(maintainer.id), data={})
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Maintainer.objects.count() == 1
        assert Maintainer.objects.first().first_name == "Test"
        assert Maintainer.objects.first().last_name == "Test"
        assert Maintainer.objects.first().social_networks.count() == 2
        response: Response = client.patch(
            self.url(maintainer.id),
            data={
                "first_name": "Maintainer",
                "last_name": "Maintainer",
                "social_networks": [],
            },
            format="json",
        )
        assert response.status_code == 200
        assert Maintainer.objects.count() == 1
        assert Maintainer.objects.first().first_name == "Maintainer"
        assert Maintainer.objects.first().last_name == "Maintainer"
        assert Maintainer.objects.first().social_networks.count() == 0


@mark.django_db
class TestDeleteEndpoint:
    def url(self, maintainer_id: int) -> str:
        return reverse(
            "maintainers:maintainers-detail",
            kwargs={"pk": maintainer_id},
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/maintainers/1/"

    def test_fails_as_unauthenticated(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        client: APIClient = APIClient()
        response: Response = client.delete(self.url(maintainer.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.delete(self.url(maintainer.id))
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        maintainer: Maintainer = MaintainerFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Maintainer.objects.count() == 1
        response: Response = client.delete(self.url(maintainer.id))
        assert response.status_code == 204
        assert Maintainer.objects.count() == 0
