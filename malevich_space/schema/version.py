from pydantic import BaseModel


class VersionSchema(BaseModel):
    uid: str | None = None
    readable_name: str | None = None
    updates_markdown: str | None = None
    status: str | None = None

    def __str__(self) -> str:
        return f"<uid={self.uid}, readableName={self.readable_name}>"


class LoadedVersionSchema(VersionSchema):
    uid: str
    readable_name: str
    updates_markdown: str | None
