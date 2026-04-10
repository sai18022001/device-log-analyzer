from pydantic import BaseModel
from typing import Optional

class LogResponse(BaseModel):
    id: int
    timestamp: str
    device_id: str
    severity: str
    message: str

    class Config:
        from_attributes = True

class SummaryItem(BaseModel):
    device_id: str
    INFO: int
    WARN: int
    ERROR: int