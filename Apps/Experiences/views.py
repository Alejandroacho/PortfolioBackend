from django.db.models import QuerySet
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from Experiences.models import Experience
from Experiences.serializers import ExperienceSerializer


class ExperienceViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows to interact with Experience model
    """

    queryset: QuerySet = Experience.objects.all()
    lookup_url_kwarg: str = "pk"
    serializer_class = ExperienceSerializer
    permission_classes = [AllowAny]
