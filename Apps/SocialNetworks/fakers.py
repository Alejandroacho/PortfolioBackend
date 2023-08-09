from SocialNetworks.choices import SocialNetworks
from SocialNetworks.factories import SocialNetworkFactory


class SocialNetworkFaker(SocialNetworkFactory):
    social_network_platform: str = SocialNetworks.LINKEDIN.value
    nickname: str = "Username"
    url: str = "https://www.linkedin.com/in/username/"
