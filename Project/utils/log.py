from datetime import datetime
from logging import Logger
from logging import getLogger

from django.db.models import Model


logger: Logger = getLogger(__name__)


def log_information(event: str, instance: Model) -> None:
    """
    Log information about an action over an instance
    """
    now: datetime = datetime.now()
    class_name: str = instance.__class__.__name__
    introduction: str = f"{class_name}s App | {class_name}"
    message: str = f'{introduction} "{instance.id}" {event} at {now}'
    logger.info(message)
