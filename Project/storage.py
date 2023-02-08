from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from storages.backends.s3boto3 import S3Boto3Storage


class FileStorage(S3Boto3Storage):
    access_key: str = settings.AWS_ACCESS_KEY_ID
    secret_key: str = settings.AWS_SECRET_ACCESS_KEY
    region_name: str = settings.AWS_S3_REGION_NAME
    signature_version: str = settings.AWS_S3_SIGNATURE_VERSION


class ImageStorage(FileStorage):
    bucket_name: str = settings.AWS_STORAGE_IMAGE_BUCKET_NAME


class DocumentStorage(FileStorage):
    bucket_name: str = settings.AWS_STORAGE_DOCUMENT_BUCKET_NAME


class FilePathHandler:
    file_names_mapping: dict = {
        # Default: instance model name in lower case
        "Profile": "profile_image_of_user",
    }
    id_in_file_mapping: dict = {
        # Default: instance id
        "Profile": "user_id",
    }
    folder_names_mapping: dict = {
        # Default: instance model name in lower case + file_type
        "Image": "image"
    }
    id_in_folder_mapping: dict = {
        # Default: instance id
    }

    def __init__(self, instance: Model, filename: str, file_type: str) -> None:
        self.instance: Model = instance
        self.filename: str = filename
        self.file_type: str = file_type

    @property
    def model_name(self) -> str:
        return self.instance._meta.model.__name__

    @property
    def file_name(self) -> str:
        return self.file_names_mapping.get(
            self.model_name, self.model_name.lower()
        )

    @property
    def id_in_file(self) -> int:
        attribute: str = self.id_in_file_mapping.get(self.model_name, "id")
        return (
            getattr(self.instance, attribute, self.instance.pk)
            or self.get_last_id()
        )

    @property
    def full_file_name(self) -> str:
        extension: str = self.filename.split(".")[-1]
        return f"{self.file_name}_{self.id_in_file}.{extension}"

    @property
    def folder_name(self) -> str:
        return self.folder_names_mapping.get(
            self.model_name, f"{self.model_name.lower()}_{self.file_type}"
        )

    @property
    def id_in_folder(self) -> int:
        attribute: str = self.id_in_folder_mapping.get(self.model_name, "id")
        return (
            getattr(self.instance, attribute, self.instance.pk)
            or self.get_last_id()
        )

    def get_last_id(self) -> int:
        content_type: ContentType = ContentType.objects.get(
            model=self.model_name
        )
        model_class: Model = content_type.model_class()
        last_id: int = model_class.objects.values_list("id", flat=True).last()
        return last_id + 1 if last_id else 1

    def get_file_path(self) -> str:
        return (
            f"{self.folder_name}/"
            + f"{self.id_in_folder}/"
            + f"{self.full_file_name}"
        )


def image_file_upload(instance: Model, filename: str) -> str:
    return file_upload(instance, filename, "images")


def document_file_upload(instance: Model, filename: str) -> str:
    return file_upload(instance, filename, "documents")


def file_upload(instance: Model, filename: str, type: str) -> str:
    path_handler: FilePathHandler = FilePathHandler(instance, filename, type)
    if not are_aws_variables_set():
        base_path: str = f"{settings.MEDIA_PATH}/"
    return f"{base_path or ''}{path_handler.get_file_path()}"


def get_image_storage() -> ImageStorage or None:
    return None if not are_aws_variables_set() else ImageStorage()


def get_document_storage() -> DocumentStorage or None:
    return None if not are_aws_variables_set() else DocumentStorage()


def are_aws_variables_set() -> bool:
    return (
        settings.AWS_ACCESS_KEY_ID
        and settings.AWS_SECRET_ACCESS_KEY
        and settings.AWS_STORAGE_IMAGE_BUCKET_NAME
        and settings.AWS_S3_REGION_NAME
        and settings.AWS_S3_SIGNATURE_VERSION
    )
