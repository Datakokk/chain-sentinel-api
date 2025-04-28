from pydantic import BaseModel

class TransactionSchema(BaseModel):
    hash: str
    from_address: str
    to_address: str
    value: int
    timestamp: str

    class Config:
        from_attributes = True