from typing import Sequence, Optional

from pydantic import BaseModel

from .dep import DepSchema, LoadedDepSchema
from .schema import LoadedSchemaSchema


class OpArg(BaseModel):
    arg_name: Optional[str]
    arg_type: Optional[str]
    arg_order: Optional[int]


class OpSchema(BaseModel):
    core_id: str
    type: str

    input_schema: Sequence[str] = []
    output_schema: Sequence[str] = []
    requires: Sequence[DepSchema] = []


class LoadedOpSchema(OpSchema):
    uid: str
    name: Optional[str]
    doc: Optional[str]
    finish_msg: Optional[str]

    tl: Optional[int]
    query: Optional[str]
    mode: Optional[str]

    collections_names: Optional[list[str]]
    extra_collections_names: Optional[list[str]]

    collection_out_names: Optional[list[str]]

    args: Optional[list[OpArg]]

    input_schema: Sequence[LoadedSchemaSchema] = []
    output_schema: Sequence[LoadedSchemaSchema] = []
    loaded_requires: Sequence[LoadedDepSchema] = []
