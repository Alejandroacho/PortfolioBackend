from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from Experiences.models import Experience
from Images.serializers import ImageSerializer
from Technologies.serializers import TechnologySerializer


class ExperienceSerializer(ModelSerializer):

    logo = ImageSerializer()
    technologies = TechnologySerializer(many=True)
    time_of_experience: str = SerializerMethodField(method_name="get_time")

    @staticmethod
    def get_time(instance: Experience) -> str:
        return instance.time_of_experience

    class Meta:
        model = Experience
        fields = "__all__"
