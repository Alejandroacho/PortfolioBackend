from django.db.models import CharField
from django.db.models import Model
from django.db.models.fields import Field


class Technology(Model):
    name: Field = CharField(max_length=100, null=False)

    def __str__(self) -> str:
        return f"{self.id} | {self.name}"

    class Meta:
        verbose_name_plural = "technologies"
