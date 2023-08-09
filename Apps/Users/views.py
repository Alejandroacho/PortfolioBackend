from django.db.models import QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet

from Users.models import User
from Users.serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows to interact with User model
    """

    queryset: QuerySet = User.objects.all()
    lookup_url_kwarg: str = "pk"
    serializer_class = UserSerializer
