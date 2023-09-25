from pydantic import BaseModel


class OrgSchema(BaseModel):
    slug: str | None = None
    name: str | None = None


class LoadedOrgSchema(BaseModel):
    uid: str | None = None
