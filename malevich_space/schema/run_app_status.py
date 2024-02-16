from pydantic import BaseModel

class RunCompStatus(BaseModel):
    in_flow_comp_id: str
    in_flow_comp_alias: str | None = None
    in_flow_app_id: str | None = None
    status: str
