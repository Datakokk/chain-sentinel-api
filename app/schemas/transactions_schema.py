from pydantic import BaseModel, Field
from typing import Optional
from pydantic import ConfigDict

class TransactionSchema(BaseModel):
    hash: str
    from_address: str
    to_address: str
    value: float
    timestamp: int
    user_id: Optional[str] = None
    status: Optional[str] = "pending"  # Default status is 'pending'
    analysis_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TransactionCreateSchema(BaseModel):
    hash: str = Field(..., description="Hash único de la transacción")
    from_address: str = Field(..., description="Dirección de origen")
    to_address: str = Field(..., description="Dirección de destino")
    value: float = Field(..., description="Cantidad transferida")
    timestamp: int = Field(..., description="Timestamp en formato UNIX")
    user_id: Optional[str] = Field(None, description="UID del usuario en Firebase")
    status: Optional[str] = Field("pending", description="Estado de la transacción")
    analysis_id: Optional[str] = Field(None, description="ID del análisis ML")
