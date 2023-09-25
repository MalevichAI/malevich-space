from pydantic import BaseModel

from .sa import SASchema, LoadedSASchema


class HostSchema(BaseModel):
    conn_url: str
    alias: str | None = None
    sa: SASchema | None = None


# TODO if we want inheritance here, do something with type of sa
class LoadedHostSchema(BaseModel):
    conn_url: str
    alias: str | None = None
    uid: str
    sa: list[LoadedSASchema] = []
