from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Authors.models import Author
from Authors.serializers import AuthorSerializer
from Users.permissions import IsAdmin
from Users.permissions import IsVerified


class AuthorViewSet(ModelViewSet):
    queryset: QuerySet = Author.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: AuthorSerializer = AuthorSerializer
    permission_classes: list = [IsAuthenticated & IsVerified & IsAdmin]
