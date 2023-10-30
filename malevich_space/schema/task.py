from pydantic import BaseModel


class TaskSchema(BaseModel):
    pass


class LoadedTaskSchema(TaskSchema):
    uid: str
    state: str | None = None


class LoadedTaskStartSchema(BaseModel):
    in_flow_id: str | None
    ca_alias: str | None
    injected_alias: str | None
