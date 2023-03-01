from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Projects.models import Project
from Projects.serializers import ProjectSerializer
from Users.permissions import IsAdmin
from Users.permissions import IsVerified


class ProjectViewSet(ModelViewSet):
    queryset: QuerySet = Project.objects.all().order_by("-id")
    lookup_url_kwarg: str = "pk"
    serializer_class: ProjectSerializer = ProjectSerializer
    permission_classes: list = [IsAuthenticated & IsVerified & IsAdmin]
