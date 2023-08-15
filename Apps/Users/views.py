from django.db.models import QuerySet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from Users.models import User
from Users.serializers import UserSerializer


class UserViewSet(ListModelMixin, GenericViewSet):
    """
    API endpoint that allows to interact with User model
    """

    queryset: QuerySet = User.objects.all()
    lookup_url_kwarg: str = "pk"
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
