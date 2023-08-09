from django.db.models import QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet

from Authors.models import Author
from Authors.serializers import AuthorSerializer


class AuthorViewSet(ReadOnlyModelViewSet):
    queryset: QuerySet = Author.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: AuthorSerializer = AuthorSerializer
