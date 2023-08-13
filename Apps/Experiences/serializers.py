from rest_framework.serializers import ModelSerializer

from Experiences.models import Experience
from Images.serializers import ImageSerializer
from Technologies.serializers import TechnologySerializer


class ExperienceSerializer(ModelSerializer):

    logo = ImageSerializer()
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Experience
        fields = '__all__'
