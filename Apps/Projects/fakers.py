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
    def technologies(self, create, extracted, **kwargs):
        if not extracted:
            self.technologies.add(TechnologyFaker())
        else:
            super().images(create, extracted, **kwargs)

    @post_generation
    def authors(self, create, extracted, **kwargs):
        if not extracted:
            self.authors.add(AuthorFaker())
        else:
            super().images(create, extracted, **kwargs)

    @post_generation
    def images(self, create, extracted, **kwargs):
        if not extracted:
            self.images.add(ImageFaker())
        else:
            super().images(create, extracted, **kwargs)
