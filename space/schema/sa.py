from pydantic import BaseModel


class SASchema(BaseModel):
    alias: str
    core_username: str
    core_password: str
    override: bool = False


class LoadedSASchema(SASchema):
    uid: str
