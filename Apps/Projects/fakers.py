from factory import post_generation

from Authors.fakers import AuthorFaker
from Images.fakers import ImageFaker
from Projects.factories import ProjectFactory
from Technologies.fakers import TechnologyFaker


class ProjectFaker(ProjectFactory):
    title: str = "Test Project"
    description: str = "Test Description"
    url: str = "https://www.test.com"
    is_public: bool = True
    repository: str = "https://www.test.com"

    @post_generation
    def technologies(
        self, create: bool, extracted: list, **kwargs: dict
    ) -> None:
        if not extracted:
            self.technologies.add(TechnologyFaker())
        else:
            [self.technologies.add(technology) for technology in extracted]

    @post_generation
    def authors(self, create: bool, extracted: list, **kwargs: dict) -> None:
        if not extracted:
            self.authors.add(AuthorFaker())
        else:
            [self.authors.add(author) for author in extracted]

    @post_generation
    def images(self, create: bool, extracted: list, **kwargs: dict) -> None:
        if not extracted:
            self.images.add(ImageFaker())
        else:
            [self.images.add(image) for image in extracted]
