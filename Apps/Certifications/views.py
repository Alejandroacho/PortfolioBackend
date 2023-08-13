from django.db.models import QuerySet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from Certifications.models import Certification
from Certifications.serializers import CertificationSerializer


class CertificationViewSet(ListModelMixin, GenericViewSet):
    queryset: QuerySet = Certification.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: CertificationSerializer = CertificationSerializer
    permission_classes = [AllowAny]
