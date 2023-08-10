from django.db.models import QuerySet
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from Technologies.models import Technology
from Technologies.serializers import TechnologySerializer


class TechnologyViewSet(ReadOnlyModelViewSet):
    queryset: QuerySet = Technology.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: TechnologySerializer = TechnologySerializer
    permission_classes = [AllowAny]
