import re

from pydantic import BaseModel, Field


class CreateAsset(BaseModel):
    core_path: str
    is_composite: bool | None = None
    checksum: str | None = None


class Asset(CreateAsset):
    uid: str
    upload_url: str
    download_url: str | None = None
