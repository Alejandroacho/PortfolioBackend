from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Certifications.models import Certification
from Certifications.serializers import CertificationSerializer
from Users.permissions import IsAdmin
from Users.permissions import IsVerified


class CertificationViewSet(ModelViewSet):
    queryset: QuerySet = Certification.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: CertificationSerializer = CertificationSerializer
    permission_classes: list = [IsAuthenticated & IsVerified & IsAdmin]
