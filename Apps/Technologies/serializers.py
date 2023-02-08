from django.db.models import Model
from rest_framework.serializers import ModelSerializer

from Technologies.models import Technology


class TechnologySerializer(ModelSerializer):
    class Meta:
        model: Model = Technology
        fields: str = "__all__"
        read_only_fields: list = ["id"]
