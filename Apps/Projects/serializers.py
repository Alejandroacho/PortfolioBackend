from django.db.models import Model
from rest_framework.serializers import ModelSerializer

from Authors.models import Author
from Authors.serializers import AuthorSerializer
from Images.models import Image
from Images.serializers import ImageSerializer
from Projects.models import Project
from Technologies.models import Technology
from Technologies.serializers import TechnologySerializer


class ProjectSerializer(ModelSerializer):
    authors = AuthorSerializer(many=True)
    images = ImageSerializer(many=True)
    technologies = TechnologySerializer(many=True)

    class Meta:
        model: Model = Project
        fields: str = "__all__"
        read_only_fields: list = ["id"]
        allow_empty_fields: list = ["authors", "images", "technologies"]

    def to_representation(self, instance: Project) -> dict:
        return {
            "id": instance.id,
            "title": instance.title,
            "introduction": instance.introduction,
            "description": instance.description,
            "url": instance.url,
            "repository": instance.repository,
            "authors": AuthorSerializer(instance.authors.all(), many=True).data,
            "images": ImageSerializer(instance.images.all(), many=True).data,
            "technologies": TechnologySerializer(
                instance.technologies.all(), many=True
            ).data,
        }
