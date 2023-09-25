from pydantic import BaseModel

from .status import CIStatus
from .platform import CIPlatform


class CIReportSetup(BaseModel):
    config_path: str
    comp_dir: str
    platform: CIPlatform


class CIReport(BaseModel):
    branch: str
    commit_digest: str
    commit_message: str
    status: CIStatus
    image: str
