from django.db.models import Field
from django.db.models import Model
from rest_framework.serializers import CharField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ModelSerializer

from Technologies.models import Technology


class TechnologySerializer(ModelSerializer):
    id: Field = IntegerField(read_only=True)
    name: Field = CharField()

    class Meta:
        model: Model = Technology
        fields: str = "__all__"
