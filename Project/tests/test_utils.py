import logging
from datetime import datetime
from logging import Logger

from freezegun import freeze_time
from mock import MagicMock
from mock import PropertyMock
from pytest import mark

from Project.utils.log import log_information


@mark.django_db
class TestAppUtils:
    @freeze_time("2012-01-14")
    def test_log_information(self, caplog: Logger) -> None:
        caplog.clear()
        caplog.set_level(logging.INFO)
        instance: MagicMock = MagicMock()
        id: PropertyMock = PropertyMock(return_value=1)
        type(instance).id = id
        log_information("test", instance)
        now: datetime = datetime.now()
        introduction: str = f"MagicMocks App | MagicMock"
        test_instance: int = 1
        expected_message: str = (
            f'{introduction} "{test_instance}" test at {now}'
        )
        assert expected_message in caplog.text
