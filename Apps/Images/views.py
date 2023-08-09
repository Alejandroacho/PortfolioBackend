from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ReadOnlyModelViewSet

from Images.models import Image
from Images.serializers import ImageSerializer


@extend_schema_view(list=extend_schema(description='Get all Images'))
class ImageViewSet(ReadOnlyModelViewSet):
    queryset: QuerySet = Image.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: ImageSerializer = ImageSerializer

