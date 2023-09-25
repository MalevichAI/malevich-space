from typing import Dict, Any

from pydantic import BaseModel


class CfgSchema(BaseModel):
    readable_name: str
    core_name: str | None = None
    cfg_json: Dict[str, Any]


class LoadedCfgSchema(CfgSchema):
    uid: str
