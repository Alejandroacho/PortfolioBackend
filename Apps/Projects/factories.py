from django.db.models import Model
from factory import post_generation
from factory.django import DjangoModelFactory

from Projects.models import Project


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model: Model = Project

    @post_generation
    def technologies(self, create, extracted, **kwargs):
        if extracted and isinstance(extracted, list):
            self.technologies.add(*extracted)
        if not extracted and isinstance(extracted, int):
            self.technologies.add(extracted)

    @post_generation
    def authors(self, create, extracted, **kwargs):
        if extracted and isinstance(extracted, list):
            self.authors.add(*extracted)
        if not extracted and isinstance(extracted, int):
            self.authors.add(extracted)

    @post_generation
    def images(self, create, extracted, **kwargs):
        if extracted and isinstance(extracted, list):
            self.images.add(*extracted)
        if not extracted and isinstance(extracted, int):
            self.images.add(extracted)
