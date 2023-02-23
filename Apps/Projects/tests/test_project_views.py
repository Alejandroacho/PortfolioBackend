import base64
from io import BufferedReader

import pytest
from django.conf import settings
from django.urls import reverse
from pytest import fixture
from rest_framework.response import Response
from rest_framework.test import APIClient

from Authors.fakers import AuthorFaker
from Authors.serializers import AuthorSerializer
from Images.fakers import ImageFaker
from Images.serializers import ImageSerializer
from Projects.fakers import ProjectFaker
from Projects.models import Project
from Technologies.fakers import TechnologyFaker
from Technologies.serializers import TechnologySerializer
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


@fixture(scope="class")
def base64_image() -> bytes:
    image_file: BufferedReader = open(f"{settings.STATIC_PATH}/logo.png", "rb")
    image_base64: bytes = base64.b64encode(image_file.read())
    image_file.close()
    return image_base64


@pytest.mark.django_db
class TestCreateEndpoint:
    def url(self) -> str:
        return reverse("projects:projects-list")

    def test_url(self) -> None:
        assert self.url() == "/api/projects/"

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
        assert Project.objects.count() == 0
        response: Response = client.post(
            self.url(),
            data={
                "title": "Kotlin project",
                "description": "Kotlin project description",
                "url": "https://www.kotlin.com",
                "is_public": True,
                "repository": "https://www.kotlin.com",
                "technologies": [TechnologyFaker().id, TechnologyFaker().id],
                "authors": [AuthorFaker().id, AuthorFaker().id],
                "images": [ImageFaker().id, ImageFaker().id],
            },
            format="json",
        )
        assert response.status_code == 201
        assert Project.objects.count() == 1
        assert Project.objects.first().title == "Kotlin project"
        assert (
            Project.objects.first().description == "Kotlin project description"
        )
        assert Project.objects.first().url == "https://www.kotlin.com"
        assert Project.objects.first().is_public == True
        assert Project.objects.first().repository == "https://www.kotlin.com"
        assert Project.objects.first().technologies.count() == 2
        assert Project.objects.first().authors.count() == 2
        assert Project.objects.first().images.count() == 2

    def test_works_as_admin_without_related_models(self) -> None:
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Project.objects.count() == 0
        response: Response = client.post(
            self.url(),
            data={
                "title": "Kotlin project",
                "description": "Kotlin project description",
                "url": "https://www.kotlin.com",
                "is_public": True,
                "repository": "https://www.kotlin.com",
                "technologies": [],
                "authors": [],
                "images": [],
            },
            format="json",
        )
        assert response.status_code == 201
        assert Project.objects.count() == 1
        assert Project.objects.first().title == "Kotlin project"
        assert (
            Project.objects.first().description == "Kotlin project description"
        )
        assert Project.objects.first().url == "https://www.kotlin.com"
        assert Project.objects.first().is_public == True
        assert Project.objects.first().repository == "https://www.kotlin.com"
        assert Project.objects.first().technologies.count() == 0
        assert Project.objects.first().authors.count() == 0
        assert Project.objects.first().images.count() == 0


@pytest.mark.django_db
class TestRetrieveEndpoint:
    def url(self, project_id: int = None) -> str:
        return (
            reverse("projects:projects-detail", kwargs={"pk": project_id})
            if project_id
            else reverse("projects:projects-list")
        )

    def test_url(self) -> None:
        assert self.url(1) == "/api/projects/1/"
        assert self.url() == "/api/projects/"

    def test_fails_as_unauthenticated(self) -> None:
        project: Project = ProjectFaker()
        client: APIClient = APIClient()
        response: Response = client.get(self.url(project.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        project: Project = ProjectFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(project.id))
        assert response.status_code == 403

    def test_retrieve_works_as_admin(self) -> None:
        project: Project = ProjectFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url(project.id))
        assert response.status_code == 200
        assert response.data["id"] == project.id
        assert response.data["title"] == project.title
        assert response.data["description"] == project.description
        assert response.data["url"] == project.url
        assert response.data["is_public"] == project.is_public
        assert response.data["repository"] == project.repository
        assert (
            response.data["technologies"]
            == TechnologySerializer(project.technologies.all(), many=True).data
        )
        assert (
            response.data["authors"]
            == AuthorSerializer(project.authors.all(), many=True).data
        )
        assert (
            response.data["images"]
            == ImageSerializer(project.images.all(), many=True).data
        )

    def test_list_works_as_admin(self) -> None:
        project: Project = ProjectFaker()
        project2: Project = ProjectFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.get(self.url())
        assert response.status_code == 200
        assert response.data[1]["id"] == project.id
        assert response.data[1]["title"] == project.title
        assert response.data[1]["description"] == project.description
        assert response.data[1]["url"] == project.url
        assert response.data[1]["is_public"] == project.is_public
        assert response.data[1]["repository"] == project.repository
        assert (
            response.data[1]["technologies"]
            == TechnologySerializer(project.technologies.all(), many=True).data
        )
        assert (
            response.data[1]["authors"]
            == AuthorSerializer(project.authors.all(), many=True).data
        )
        assert (
            response.data[1]["images"]
            == ImageSerializer(project.images.all(), many=True).data
        )
        assert response.data[0]["id"] == project2.id
        assert response.data[0]["title"] == project2.title
        assert response.data[0]["description"] == project2.description
        assert response.data[0]["url"] == project2.url
        assert response.data[0]["is_public"] == project2.is_public
        assert response.data[0]["repository"] == project2.repository
        assert (
            response.data[0]["technologies"]
            == TechnologySerializer(project2.technologies.all(), many=True).data
        )
        assert (
            response.data[0]["authors"]
            == AuthorSerializer(project2.authors.all(), many=True).data
        )
        assert (
            response.data[0]["images"]
            == ImageSerializer(project2.images.all(), many=True).data
        )


@pytest.mark.django_db
class TestUpdateEndpoint:
    def url(self, project_id: int) -> str:
        return reverse("projects:projects-detail", kwargs={"pk": project_id})

    def test_url(self) -> None:
        assert self.url(1) == "/api/projects/1/"

    def test_fails_as_unauthenticated(self) -> None:
        project: Project = ProjectFaker()
        client: APIClient = APIClient()
        response: Response = client.put(self.url(project.id), data={})
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        project: Project = ProjectFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.put(self.url(project.id), data={})
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        project: Project = ProjectFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Project.objects.count() == 1
        assert Project.objects.first().title == "Test Project"
        response: Response = client.put(
            self.url(project.id),
            data={"title": "Kotlin Project"},
            format="json",
        )
        assert response.status_code == 200
        assert Project.objects.count() == 1
        assert Project.objects.first().title == "Kotlin Project"


@pytest.mark.django_db
class TestDeleteEndpoint:
    def url(self, project_id: int) -> str:
        return reverse("projects:projects-detail", kwargs={"pk": project_id})

    def test_url(self) -> None:
        assert self.url(1) == "/api/projects/1/"

    def test_fails_as_unauthenticated(self) -> None:
        project: Project = ProjectFaker()
        client: APIClient = APIClient()
        response: Response = client.delete(self.url(project.id))
        assert response.status_code == 401

    def test_fails_as_unverified(self) -> None:
        project: Project = ProjectFaker()
        user: User = UserFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        response: Response = client.delete(self.url(project.id))
        assert response.status_code == 403

    def test_works_as_admin(self) -> None:
        project: Project = ProjectFaker()
        user: User = AdminFaker()
        client: APIClient = APIClient()
        client.force_authenticate(user)
        assert Project.objects.count() == 1
        response: Response = client.delete(self.url(project.id))
        assert response.status_code == 204
        assert Project.objects.count() == 0
