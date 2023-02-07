from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import FileField
from django.db.models import ForeignKey
from django.db.models import ForeignObject
from django.db.models import Model
from django.db.models import TextField
from django.db.models import URLField
from django.db.models.fields import Field
from django_mysql.models import ListCharField

from Images.models import Image
from Project.storage import document_file_upload
from Project.storage import get_document_storage


class Certification(Model):
    name: Field = CharField(max_length=100, null=False)
    description: Field = TextField(null=False)
    tags: ListCharField = ListCharField(
        base_field=CharField(max_length=20),
        null=True,
        size=10,
        max_length=(400),
    )
    url: Field = URLField(null=True)
    image: ForeignObject = ForeignKey(
        Image,
        null=True,
        on_delete=CASCADE,
    )
    file: Field = FileField(
        "File",
        storage=get_document_storage(),
        upload_to=document_file_upload,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.name}"
