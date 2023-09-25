from typing import Sequence

from pydantic import BaseModel

from .dep import DepSchema, LoadedDepSchema
from .schema import LoadedSchemaSchema


class OpSchema(BaseModel):
    core_id: str
    type: str
    input_schema: Sequence[str] = []
    output_schema: Sequence[str] = []
    requires: Sequence[DepSchema] = []


class LoadedOpSchema(OpSchema):
    uid: str
    input_schema_model: Sequence[LoadedSchemaSchema] = []
    output_schema_model: Sequence[LoadedSchemaSchema] = []
    loaded_requires: Sequence[LoadedDepSchema] = []
