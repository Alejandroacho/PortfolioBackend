from django.db.models import Model
from factory import post_generation
from factory.django import DjangoModelFactory

from Experiences.models import Experience


class ExperienceFactory(DjangoModelFactory):
    current: bool = False

    @post_generation
    def technologies(self, create, extracted, **kwargs):
        if extracted and isinstance(extracted, list):
            self.technologies.add(*extracted)

    class Meta:
        model: Model = Experience
