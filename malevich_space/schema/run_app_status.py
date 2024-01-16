from pydantic import BaseModel

class RunCompStatus(BaseModel):
    in_flow_comp_id: int
    in_flow_app_id: int
    status: str
