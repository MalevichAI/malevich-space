import urllib.parse

from pydantic import BaseModel

from malevich_space import constants

from .host import HostSchema


class SpaceSetup(BaseModel):
    api_url: str

    username: str | None = None
    password: str | None = None
    token: str | None = None
    org: str | None = None

    host: HostSchema = HostSchema(conn_url=constants.PUBLIC_CLOUD_CONN_URL)

    graphql_path: str = constants.GRAPHQL_PATH
    auth_path: str = constants.AUTH_PATH
    api_gateway_path: str = constants.API_GATEWAY_PATH

    @staticmethod
    def _replace_url_scheme(url: str, new_scheme: str) -> str:
        # Parse the input URL
        parsed_url = urllib.parse.urlparse(url)
        new_url_tuple = (
            new_scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment
        )
        # Construct the new URL with the updated scheme
        new_url = urllib.parse.urlunparse(new_url_tuple)
        return new_url

    def __repr__(self) -> str:
        return f"{self.api_url}"

    def __str__(self) -> str:
        return f"{self.api_url}"

    def graphql_url(self) -> str:
        return f"{self.api_url}{self.graphql_path}"

    def auth_url(self) -> str:
        return f"{self.api_url}{self.auth_path}"

    def ws_url(self) -> str:
        return f"{self._replace_url_scheme(self.api_url, 'wss')}{self.graphql_path}"
    
    def api_gateway_url(self) -> str:
        return f"{self.api_url}{self.api_gateway_path}"


class Setup(BaseModel):
    space: SpaceSetup
