from pydantic import BaseModel, ConfigDict, Field
from typing import List


class EtherscanTransaction(BaseModel):
    hash: str
    from_address: str = Field(alias="from")
    to_address: str = Field(alias="to")
    value: int = Field(alias="value")
    timeStamp: str  # nota: Etherscan usa camelCase aquí

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class EtherscanResponse(BaseModel):
    status: str
    message: str
    result: List[EtherscanTransaction]

    model_config = ConfigDict(extra="allow")
