from pydantic import BaseModel

from .host import HostSchema


class SpaceSetup(BaseModel):
    auth_url: str
    gql_url: str
    host: HostSchema
    username: str | None = None
    password: str | None = None
    token: str | None = None
    ws_url: str | None = None
    org: str | None = None

    def __repr__(self) -> str:
        return f"{self.gql_url}"

    def __str__(self) -> str:
        return f"{self.gql_url}"


class Setup(BaseModel):
    space: SpaceSetup
