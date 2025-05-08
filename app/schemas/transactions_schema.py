from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TransactionSchema(BaseModel):
    hash: str
    from_address: str = Field(alias="from")
    to_address: str = Field(alias="to")
    value: int = Field(alias="value")
    timestamp: str = Field(alias="timeStamp")

    model_config = ConfigDict(extra="allow",from_attributes=True, populate_by_name=True)

class TransactionCreateSchema(BaseModel):
    hash: str = Field(..., description="Hash único de la transacción")
    from_address: str = Field(..., description="Dirección de origen")
    to_address: str = Field(..., description="Dirección de destino")
    value: float = Field(..., description="Cantidad transferida")
    timestamp: Optional[int] = Field(None, description="Timestamp de la transacción (opcional)")
