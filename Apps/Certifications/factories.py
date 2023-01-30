from django.db.models import Model
from factory.django import DjangoModelFactory

from Certifications.models import Certification


class CertificationFactory(DjangoModelFactory):
    class Meta:
        model: Model = Certification
