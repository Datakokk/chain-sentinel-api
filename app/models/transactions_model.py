from pydantic import BaseModel, ConfigDict

class Transaction(BaseModel):
    hash: str
    from_address: str
    to_address: str
    value: int
    timestamp: str

    model_config = ConfigDict(from_attributes=True)
