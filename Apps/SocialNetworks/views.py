from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Project.permissions import IsGetPetition
from SocialNetworks.models import SocialNetwork
from SocialNetworks.serializers import SocialNetworkSerializer
from Users.permissions import IsAdmin
from Users.permissions import IsVerified


class SocialNetworkViewSet(ModelViewSet):
    queryset: QuerySet = SocialNetwork.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: SocialNetworkSerializer = SocialNetworkSerializer
    permission_classes: list = [
        (IsAuthenticated & IsVerified & IsAdmin) | IsGetPetition
    ]
