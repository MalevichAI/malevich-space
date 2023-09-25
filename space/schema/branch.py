from pydantic import BaseModel

from .version import LoadedVersionSchema


class BranchSchema(BaseModel):
    uid: str | None = None
    name: str | None = None
    status: str | None = None


class LoadedBranchSchema(BranchSchema):
    uid: str
    active_version: LoadedVersionSchema | None = None
