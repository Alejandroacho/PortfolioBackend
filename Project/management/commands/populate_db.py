from logging import Logger
from logging import getLogger

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser
from tqdm import trange as progress

from Authors.fakers import AuthorFaker
from Certifications.fakers import CertificationFaker
from Projects.fakers import ProjectFaker
from SocialNetworks.fakers import SocialNetworkFaker
from Technologies.fakers import TechnologyFaker
from Users.fakers import UserFaker
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

    def populate(self, instances_number: int, _: bool) -> None:
        user: User = self.create_fake_user()
        social_networks: list = self.create_fake_social_networks(
            instances_number
        )
        authors: list = self.create_fake_authors(
            user, social_networks, instances_number
        )
        technologies: list = self.create_fake_technologies(instances_number)
        self.create_fake_certifications(instances_number)
        self.create_fake_projects(authors, technologies, instances_number)

    def create_fake_user(self) -> User:
        self.stdout.write("Creating fake user")
        user: User = UserFaker(
            email="admin@admin.com",
            password="adminpassword",
        )
        self.stdout.write("Fake user created")
        return user

    def create_fake_social_networks(self, instances: int) -> list:
        self.stdout.write("Creating fake social networks")
        social_networks: list = []
        for _ in progress(instances):
            social_networks.append(SocialNetworkFaker())
        self.stdout.write("Fake social networks created")
        return social_networks

    def create_fake_authors(
        self, user: User, social_networks: list, instances: int
    ) -> list:
        self.stdout.write("Creating fake authors")
        authors: list = []
        AuthorFaker(
            first_name=user.first_name,
            last_name=user.last_name,
            social_networks=social_networks
        )
        for _ in progress(instances):
            authors.append(AuthorFaker())
        self.stdout.write("Fake authors created")
        return authors

    def create_fake_certifications(self, instances: int) -> None:
        self.stdout.write("Creating fake certifications")
        for _ in progress(instances):
            CertificationFaker()
        self.stdout.write("Fake certifications created")

    def create_fake_technologies(self, instances: int) -> list:
        self.stdout.write("Creating fake technologies")
        technologies: list = []
        for _ in progress(instances):
            technologies.append(TechnologyFaker())
        self.stdout.write("Fake technologies created")
        return technologies

    def create_fake_projects(
        self, authors: list, technologies: list, instances: int
    ) -> None:
        self.stdout.write("Creating fake projects")
        for _ in progress(instances):
            ProjectFaker(technologies=technologies, authors=authors)
        self.stdout.write("Fake projects created")
