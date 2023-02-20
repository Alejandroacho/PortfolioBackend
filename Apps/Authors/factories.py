from django.db.models import Model
from factory.django import DjangoModelFactory

from Authors.models import Author


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model: Model = Author
