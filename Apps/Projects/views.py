from django.db.models import QuerySet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from Projects.models import Project
from Projects.serializers import ProjectSerializer


class ProjectViewSet(ListModelMixin, GenericViewSet):
    queryset: QuerySet = Project.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: ProjectSerializer = ProjectSerializer
    permission_classes = [AllowAny]
