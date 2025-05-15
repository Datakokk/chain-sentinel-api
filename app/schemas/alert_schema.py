from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AlertCreate(BaseModel):
    from_address: Optional[str] = Field(None, description="Origin address of the alert")
    to_address: Optional[str] = Field(None, description="Destination address of the alert")
    message: str
    type: str
    transaction_hash: Optional[str]
    value: Optional[float]
    severity: Optional[str]
    timestamp: Optional[datetime]
    crated_at: Optional[datetime] = None #automatically set to the current time
