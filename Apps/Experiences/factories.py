from django.db.models import Model
from factory.django import DjangoModelFactory

from Experiences.models import Experience


class ExperienceFactory(DjangoModelFactory):
    current: bool = False

    class Meta:
        model: Model = Experience
