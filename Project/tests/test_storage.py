from uuid import UUID

from django.test import override_settings
from mock import patch
from mock.mock import MagicMock
from pytest import mark

from Project.storage import DocumentStorage
from Project.storage import FilePathHandler
from Project.storage import ImageStorage
from Project.storage import are_aws_variables_set
from Project.storage import document_file_upload
from Project.storage import get_document_storage
from Project.storage import get_image_storage
from Project.storage import image_file_upload
from Users.factories import UserFactory
from Users.fakers import UserFaker
from Users.models import User


class TestProjectStorage:
    @override_settings(AWS_ACCESS_KEY_ID=None)
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME="test")
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_aws_variables_set_returns_False_if_one_is_None(self) -> None:
        assert not are_aws_variables_set()

    @override_settings(AWS_ACCESS_KEY_ID="test")
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME="test")
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_aws_variables_set_returns_True_if_all_are_set(self) -> None:
        assert are_aws_variables_set()

    @override_settings(AWS_ACCESS_KEY_ID="test")
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME="test")
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_get_image_storage_returns_ImageStorage_instance_if_aws_keys_are_set(
        self,
    ) -> None:
        assert isinstance(get_image_storage(), ImageStorage)

    @override_settings(AWS_ACCESS_KEY_ID="test")
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME="test")
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_get_document_storage_returns_ImageStorage_instance_if_aws_keys_are_set(
        self,
    ) -> None:
        assert isinstance(get_document_storage(), DocumentStorage)

    @override_settings(AWS_ACCESS_KEY_ID="test")
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME=None)
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_get_image_storage_returns_None_if_a_aws_keys_is_not_set(
        self,
    ) -> None:
        assert not get_image_storage()

    @override_settings(AWS_ACCESS_KEY_ID="test")
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME=None)
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_get_document_storage_returns_None_if_a_aws_keys_is_not_set(
        self,
    ) -> None:
        assert not get_document_storage()


@mark.django_db
class TestFilePathHandler:
    def test_model_name_returns_model_name(self) -> None:
        assert FilePathHandler(UserFaker(), None, None).model_name == "User"

    def test_file_name_returns_default_file_name(self) -> None:
        path_handler: FilePathHandler = FilePathHandler(UserFaker(), None, None)
        assert path_handler.file_name == "user"

    def test_id_in_file_returns_uuid_in_file(self) -> None:
        user: User = UserFaker()
        path_handler: FilePathHandler = FilePathHandler(user, None, None)
        assert isinstance(path_handler.id_in_file, UUID)

    def test_full_file_name(self) -> None:
        user: User = UserFaker()
        file_name: str = "example_file_name.png"
        path_handler: FilePathHandler = FilePathHandler(user, file_name, None)
        assert ".png" in path_handler.full_file_name

    def test_folder_name_returns_default_folder_name(self) -> None:
        path_handler: FilePathHandler = FilePathHandler(
            UserFaker(), None, "images"
        )
        assert path_handler.folder_name == "users"

    def test_folder_name_returns_custom_folder_name(self) -> None:
        path_handler: FilePathHandler = FilePathHandler(
            UserFaker(), None, "images"
        )
        assert path_handler.folder_name == "users"

    def test_id_in_folder_returns_default_id_in_folder(self) -> None:
        user: User = UserFaker()
        path_handler: FilePathHandler = FilePathHandler(user, None, "images")
        assert path_handler.id_in_folder == user.id

    def test_get_last_id_with_instances_in_db(self) -> None:
        user: User = UserFaker()
        non_saved_user: User = UserFactory.build(email="user@appname.me")
        path_handler: FilePathHandler = FilePathHandler(
            non_saved_user, None, "images"
        )
        assert path_handler.get_last_id() == user.id + 1

    def test_get_last_id_without_instances_in_db(self) -> None:
        non_saved_user: User = UserFactory.build(email="user@appname.me")
        path_handler: FilePathHandler = FilePathHandler(
            non_saved_user, None, "images"
        )
        assert path_handler.get_last_id() == 1

    def test_get_file_path(self) -> None:
        user: User = UserFaker()
        file_name: str = "example_file_name.png"
        path_handler: FilePathHandler = FilePathHandler(
            user, file_name, "images"
        )
        assert "users" in path_handler.get_file_path()
        assert str(user.id) in path_handler.get_file_path()
        assert "images" in path_handler.get_file_path()
        assert ".png" in path_handler.get_file_path()


@mark.django_db
class TestFileUploadFunctions:
    @patch("Project.storage.FilePathHandler.get_file_path")
    def test_image_file_upload(self, get_file_path: MagicMock) -> None:
        user: User = UserFaker()
        assert isinstance(image_file_upload(user, "image.png"), str)
        assert get_file_path.called_once()

    @patch("Project.storage.FilePathHandler.get_file_path")
    def test_document_file_upload(self, get_file_path: MagicMock) -> None:
        user: User = UserFaker()
        assert isinstance(document_file_upload(user, "document.pdf"), str)
        assert get_file_path.called_once()
