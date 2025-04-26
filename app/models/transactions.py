from pydantic import BaseModel
from typing import Optional

class Transaction(BaseModel):
    blockNumber: Optional[str]
    timeStamp: Optional[str]
    hash: Optional[str]
    nonce: Optional[str]
    blockHash: Optional[str]
    transactionIndex: Optional[str]
    from_address: Optional[str]
    to_address: Optional[str]
    value: Optional[str]
    gas: Optional[str]
    gasPrice: Optional[str]
    isError: Optional[str]
    txreceipt_status: Optional[str]
    contractAddress: Optional[str]
    cumulativeGasUsed: Optional[str]
    gasUsed: Optional[str]
    confirmations: Optional[str]
    methodId: Optional[str]
    functionName: Optional[str]

    class Config:
        orm_mode = True
