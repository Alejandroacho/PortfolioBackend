from django.db.models import QuerySet
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from SocialNetworks.models import SocialNetwork
from SocialNetworks.serializers import SocialNetworkSerializer


class SocialNetworkViewSet(ReadOnlyModelViewSet):
    queryset: QuerySet = SocialNetwork.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: SocialNetworkSerializer = SocialNetworkSerializer
    permission_classes = [AllowAny]
