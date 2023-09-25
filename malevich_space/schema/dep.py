from typing import List

from pydantic import BaseModel


class DepSchema(BaseModel):
    key: str
    type: List[str]


class LoadedDepSchema(DepSchema):
    uid: str
