import pytest

from SocialNetworks.factories import SocialNetworkFactory
from SocialNetworks.fakers import SocialNetworkFaker
from SocialNetworks.models import SocialNetwork


@pytest.mark.django_db
class TestTechnologyModel:
    def test_model_keys(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        assert hasattr(social_network, "id")
        assert hasattr(social_network, "platform")
        assert hasattr(social_network, "nickname")
        assert hasattr(social_network, "url")

    def test_str_representation(self) -> None:
        social_network: SocialNetwork = SocialNetworkFaker()
        assert (
            str(social_network)
            == f"{social_network.id} | {social_network.nickname}"
            + f" - {social_network.platform}"
        )


@pytest.mark.django_db
class TestTechnologyFactory:
    def test_factory_creates_an_instance(self) -> None:
        assert SocialNetwork.objects.count() == 0
        social_network: SocialNetwork = SocialNetworkFactory(
            platform="TIKTOK",
            nickname="User",
            url="https://www.tiktok.com/@user",
        )
        assert isinstance(social_network, SocialNetwork)
        assert SocialNetwork.objects.count() == 1


@pytest.mark.django_db
class TestTechnologyFaker:
    def test_faker_create_the_default_python_instance(self) -> None:
        assert SocialNetwork.objects.count() == 0
        social_network: SocialNetwork = SocialNetworkFaker()
        assert isinstance(social_network, SocialNetwork)
        assert SocialNetwork.objects.count() == 1
        assert social_network.nickname == "Username"
        assert social_network.platform == "LINKEDIN"
        assert social_network.url == "https://www.linkedin.com/in/username/"
