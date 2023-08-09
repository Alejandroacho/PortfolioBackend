from django.db.models import QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet

from Certifications.models import Certification
from Certifications.serializers import CertificationSerializer


class CertificationViewSet(ReadOnlyModelViewSet):
    queryset: QuerySet = Certification.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: CertificationSerializer = CertificationSerializer
