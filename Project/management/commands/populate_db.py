from logging import Logger
from logging import getLogger

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser
from tqdm import tqdm
from tqdm import trange as progress

from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.models import User


logger: Logger = getLogger(__name__)


class Command(BaseCommand):

    help: str = "Populate database with fake data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-i", "--instances", type=int, default=50)
        parser.add_argument(
            "-n", "--no-admin", dest="admin", action="store_false"
        )
        parser.set_defaults(admin=True)

    def handle(self, *args: tuple, **options: dict) -> None:
        if settings.ENVIRONMENT_NAME in ["dev", "local", "test"]:
            instances_number: int = int(options["instances"])
            create_admin: bool = bool(options["admin"])
            self.populate(instances_number, create_admin)
        else:
            logger.critical(
                "This command creates fake data do NOT run this in"
                + " production environments"
            )

    def populate(self, instances_number: int, create_admin: bool) -> None:
        users: list = self.create_fake_users(instances_number)
        if create_admin:
            self.create_admin_user()

    def create_fake_users(self, instances_number: int) -> list:
        self.stdout.write("Creating fake users")
        users: list = []
        for _ in progress(instances_number):
            user: User = UserFaker()
            users.append(user)
        self.stdout.write("Fake users created")
        return users

    def create_admin_user(self) -> None:
        self.stdout.write("Creating admin user")
        AdminFaker(
            email="admin@admin.com",
            password="adminpassword",
        )
        self.stdout.write("Admin user created")
