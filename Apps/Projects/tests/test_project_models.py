import pytest

from Authors.fakers import AuthorFaker
from Images.fakers import ImageFaker
from Projects.factories import ProjectFactory
from Projects.fakers import ProjectFaker
from Projects.models import Project
from Technologies.fakers import TechnologyFaker


@pytest.mark.django_db
class TestProjectModel:
    def test_model_keys(self) -> None:
        project: Project = ProjectFaker()
        assert hasattr(project, "id")
        assert hasattr(project, "title")
        assert hasattr(project, "introduction")
        assert hasattr(project, "description")
        assert hasattr(project, "url")
        assert hasattr(project, "is_public")
        assert hasattr(project, "repository")
        assert hasattr(project, "technologies")
        assert hasattr(project, "authors")
        assert hasattr(project, "images")

    def test_str_representation(self) -> None:
        project: Project = ProjectFaker()
        assert str(project) == f"{project.id} | {project.title}"


@pytest.mark.django_db
class TestProjectFactory:
    def test_factory_creates_an_instance(self) -> None:
        assert Project.objects.count() == 0
        project: Project = ProjectFactory(
            title="Test Project",
            introduction="Test Introduction",
            description="Test Description",
            url="https://www.test.com",
            repository="https://www.test.com",
            technologies=[TechnologyFaker().id],
            authors=[AuthorFaker().id],
            images=[ImageFaker().id],
        )
        assert isinstance(project, Project)
        assert Project.objects.count() == 1


@pytest.mark.django_db
class TestProjectFaker:
    def test_faker_create_the_default_python_instance(self) -> None:
        assert Project.objects.count() == 0
        project: Project = ProjectFaker()
        assert isinstance(project, Project)
        assert Project.objects.count() == 1
        assert project.title == "Test Project"
        assert project.description == "Test Description"
        assert project.url == "https://www.test.com"
        assert project.is_public == True
        assert project.repository == "https://www.test.com"
        assert project.technologies.count() == 1
        assert project.authors.count() == 1
        assert project.images.count() == 1
        assert "image" in project.images.first().image.name
