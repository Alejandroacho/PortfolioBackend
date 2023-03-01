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
            "description": instance.description,
            "url": instance.url,
            "is_public": instance.is_public,
            "repository": instance.repository,
            "authors": AuthorSerializer(instance.authors.all(), many=True).data,
            "images": ImageSerializer(instance.images.all(), many=True).data,
            "technologies": TechnologySerializer(
                instance.technologies.all(), many=True
            ).data,
        }

    def to_internal_value(self, data: dict) -> dict:
        authors = data.pop("authors", [])
        images = data.pop("images", [])
        technologies = data.pop("technologies", [])
        return {
            "title": data.get("title"),
            "description": data.get("description"),
            "url": data.get("url"),
            "is_public": data.get("is_public"),
            "repository": data.get("repository"),
            "authors": Author.objects.filter(id__in=authors),
            "images": Image.objects.filter(id__in=images),
            "technologies": Technology.objects.filter(id__in=technologies),
        }

    def create(self, validated_data: dict) -> Project:
        technologies: list = validated_data.pop("technologies")
        images: list = validated_data.pop("images")
        authors: list = validated_data.pop("authors")
        project = Project.objects.create(**validated_data)
        project.technologies.set(technologies)
        project.images.set(images)
        project.authors.set(authors)
        return project

    def update(self, instance: Project, validated_data: dict) -> Project:
        technologies: list = validated_data.pop("technologies")
        images: list = validated_data.pop("images")
        authors: list = validated_data.pop("authors")
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value or getattr(instance, attribute))
        instance.technologies.set(technologies)
        instance.images.set(images)
        instance.authors.set(authors)
        instance.save()
        return instance
