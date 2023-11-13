from pydantic import BaseModel


class Payload(BaseModel):
    alias: str
    caUid: str | None = None
    docs: list[str] | None = None


class InvokePayload(BaseModel):
    payload: list[Payload]
    webhook: list[str] | None = None
