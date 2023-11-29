from typing import Any
from pydantic import BaseModel
from .collection_alias import LoadedCollectionAliasSchema

class ResultSchema(BaseModel):
    ca: LoadedCollectionAliasSchema
    raw_json: list[dict[str, Any]]
