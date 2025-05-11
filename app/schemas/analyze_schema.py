from pydantic import BaseModel, Field
from datetime import datetime

class TransactionAnalyzeRequest(BaseModel):
    id_transaccion: int
    hash: str
    count: float
    source_address: str = Field(..., alias="source_address")
    destination_address: str = Field(..., alias="destination_address")
    date: datetime

class TransactionAnalyzeResponse(BaseModel):
    id_transaccion: int
    is_fraud: bool
    risk_score: float
    analyzed_at: datetime
