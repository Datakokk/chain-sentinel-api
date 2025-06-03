from pydantic import BaseModel, Field
from datetime import datetime

class TransactionAnalyzeRequest(BaseModel):
    id_transaccion: str
    hash: str
    amount: float
    origin_address: str = Field(..., alias="origin_address")
    destination_address: str = Field(..., alias="destination_address")
    date: datetime

class TransactionAnalyzeResponse(BaseModel):
    id_transaccion: str
    is_fraud: bool
    risk_score: float
    analyzed_at: datetime
