from django.db.models import CharField
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models.fields import Field
from django.db.models.fields import TextField

from Authors.models import Author
from Images.models import Image
from Technologies.models import Technology


class Project(Model):
    title: Field = CharField(max_length=100)
    introduction: Field = TextField(max_length=155)
    description: Field = TextField(max_length=1000)
    url: Field = CharField(max_length=1000, null=True, blank=True)
    repository: Field = CharField(max_length=1000, null=True, blank=True)
    technologies: Field = ManyToManyField(Technology)
    authors: Field = ManyToManyField(Author)
    images: Field = ManyToManyField(Image, blank=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.title}"
