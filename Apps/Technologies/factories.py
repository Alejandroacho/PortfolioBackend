from django.db.models import Model
from factory.django import DjangoModelFactory

from Technologies.models import Technology


class TechnologyFactory(DjangoModelFactory):
    class Meta:
        model: Model = Technology
