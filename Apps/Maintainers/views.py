from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Maintainers.models import Maintainer
from Maintainers.serializers import MaintainerSerializer
from Project.permissions import IsGetPetition
from Users.permissions import IsAdmin
from Users.permissions import IsVerified


class MaintainerViewSet(ModelViewSet):
    queryset: QuerySet = Maintainer.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: MaintainerSerializer = MaintainerSerializer
    permission_classes: list = [
        (IsAuthenticated & IsVerified & IsAdmin) | IsGetPetition
    ]
