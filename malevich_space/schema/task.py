from pydantic import BaseModel


class TaskSchema(BaseModel):
    pass


class LoadedTaskSchema(TaskSchema):
    uid: str
    state: str | None = None
