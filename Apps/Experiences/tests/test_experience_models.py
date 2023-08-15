import pytest

from Experiences.factories import ExperienceFactory
from Experiences.fakers import ExperienceFaker
from Experiences.models import Experience
from Images.fakers import ImageFaker
from Technologies.fakers import TechnologyFaker


@pytest.mark.django_db
class TestExperienceModel:
    def test_model_keys(self) -> None:
        experience: Experience = ExperienceFaker()
        assert hasattr(experience, "id")
        assert hasattr(experience, "company")
        assert hasattr(experience, "position")
        assert hasattr(experience, "description")
        assert hasattr(experience, "url")
        assert hasattr(experience, "current")
        assert hasattr(experience, "start_date")
        assert hasattr(experience, "end_date")
        assert hasattr(experience, "logo")
        assert hasattr(experience, "technologies")

    def test_str_representation(self) -> None:
        experience: Experience = ExperienceFaker()
        assert str(experience) == f"{experience.id} | {experience.company}"


@pytest.mark.django_db
class TestExperienceFactory:
    def test_factory_creates_an_instance(self) -> None:
        assert Experience.objects.count() == 0
        experience: Experience = ExperienceFactory(
            company="TEST",
            description="This is a test experience",
            url="https://www.appname.com",
            technologies=[TechnologyFaker(), TechnologyFaker()],
            logo=ImageFaker(),
            current=True,
            start_date="2020-01-01",
            end_date="2023-01-01",
        )
        assert isinstance(experience, Experience)
        assert Experience.objects.count() == 1
        assert experience.company == "TEST"
        assert experience.description == "This is a test experience"
        assert experience.url == "https://www.appname.com"
        assert experience.current is True
        assert experience.start_date == "2020-01-01"
        assert experience.end_date == "2023-01-01"
        assert experience.technologies.count() == 2
        assert "image" in experience.logo.image.name


@pytest.mark.django_db
class TestExperienceFaker:
    def test_faker_create_the_default_python_instance(self) -> None:
        assert Experience.objects.count() == 0
        experience: Experience = ExperienceFaker()
        assert isinstance(experience, Experience)
        assert Experience.objects.count() == 1
        assert experience.company == "Test Company"
