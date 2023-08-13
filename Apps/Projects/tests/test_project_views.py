import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from Authors.serializers import AuthorSerializer
from Images.serializers import ImageSerializer
from Projects.fakers import ProjectFaker
from Projects.models import Project
from Technologies.serializers import TechnologySerializer


@pytest.mark.django_db
class TestRetrieveEndpoint:
    @staticmethod
    def url() -> str:
        return reverse("projects:projects-list")

    def test_url(self) -> None:
        assert self.url() == "/api/projects/"

    def test_list_works(self) -> None:
        project: Project = ProjectFaker()
        project2: Project = ProjectFaker()
        client: APIClient = APIClient()
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
