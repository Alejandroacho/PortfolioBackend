from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Images.models import Image
from Images.serializers import ImageSerializer
from Users.permissions import IsAdmin
from Users.permissions import IsVerified


class ImageViewSet(ModelViewSet):
    queryset: QuerySet = Image.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: ImageSerializer = ImageSerializer
    permission_classes: list = [IsAuthenticated & IsVerified & IsAdmin]
