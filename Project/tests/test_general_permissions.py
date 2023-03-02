from mock import MagicMock
from mock import PropertyMock
from pytest import mark

from Project.permissions import IsGetPetition


@mark.django_db
class TestIsAdminPermission:
    def test_returns_false_if_request_is_not_get(self) -> None:
        request: MagicMock = MagicMock()
        mocked_method: PropertyMock = PropertyMock(return_value="POST")
        type(request).method = mocked_method
        assert IsGetPetition().has_permission(request, None) is False

    def test_returns_true_if_request_is_get(self) -> None:
        request: MagicMock = MagicMock()
        mocked_method: PropertyMock = PropertyMock(return_value="GET")
        type(request).method = mocked_method
        assert IsGetPetition().has_permission(request, None) is True
