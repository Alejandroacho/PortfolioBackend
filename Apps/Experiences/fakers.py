from factory import post_generation

from Experiences.factories import ExperienceFactory
from Images.fakers import ImageFaker
from Images.models import Image
from Technologies.fakers import TechnologyFaker


class ExperienceFaker(ExperienceFactory):
    company: str = "Test Company"
    position: str = "Test Position"
    description: str = "Test Description"
    url: str = "https://www.test.com"
    start_date: str = "2020-01-01"
    end_date: str = "2023-01-01"

    @post_generation
    def technologies(
        self, create: bool, extracted: list, **kwargs: dict
    ) -> None:
        if not extracted:
            self.technologies.add(TechnologyFaker())
        else:
            [self.technologies.set(technology) for technology in extracted]

    @post_generation
    def logo(self, create, extracted, **kwargs):
        if extracted:
            self.logo = extracted
        if not extracted:
            self.logo = ImageFaker()
