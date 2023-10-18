from pydantic import BaseModel


class SchemaMetadata(BaseModel):
    core_id: str | None = None
    schema_data: str | None = None


class LoadedSchemaSchema(BaseModel):
    uid: str
    core_id: str | None = None
