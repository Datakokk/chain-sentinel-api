from pydantic import BaseModel, Field, ConfigDict

class TransactionSchema(BaseModel):
    hash: str
    from_address: str = Field(alias="from")
    to_address: str = Field(alias="to")
    value: int = Field(alias="value")
    timestamp: str = Field(alias="timeStamp")

    model_config = ConfigDict(extra="allow",from_attributes=True, populate_by_name=True)
