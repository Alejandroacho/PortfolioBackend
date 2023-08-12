from django.db.models import BooleanField, ForeignObject, ForeignKey, CASCADE
from django.db.models import CharField
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models.fields import Field, DateField

from Images.models import Image
from Technologies.models import Technology


class Experience(Model):
    company: Field = CharField(max_length=100)
    position: Field = CharField(max_length=100)
    description: Field = CharField(max_length=1000)
    url: Field = CharField(max_length=1000, null=True, blank=True)
    current: Field = BooleanField(default=False)
    start_date: Field = DateField(auto_now=False, auto_now_add=False)
    end_date: Field = DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    logo: ForeignObject = ForeignKey(
        Image, null=True, on_delete=CASCADE,
    )
    technologies: Field = ManyToManyField(
        Technology, related_name="experiences"
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.company}"
