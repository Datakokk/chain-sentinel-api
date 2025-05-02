from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.blockchain_service import get_transactions_by_address
from app.firebase.firestore_client import save_transactions_batch
from app.schemas.transactions_schema import TransactionSchema
from app.schemas.etherscan_schema import EtherscanTransaction

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/{address}", response_model=List[TransactionSchema])
async def list_transactions(address: str, limit: int = Query(10, ge=1, le=100)):
    print("get_transactions_by_address:", get_transactions_by_address)

    try:
        transactions = await get_transactions_by_address(address)
        transactions = transactions[:limit]

        # Transform EtherscanTransaction objects into TransactionSchema objects
        parsed_transactions = [TransactionSchema.model_validate(tx) for tx in transactions]


        # Savve transactions to Firestore
        print("RAW TX EXAMPLE:", transactions[0])  # muestra la primera transacción
        print("TX OBJECT:", transactions[0].model_dump())
        await save_transactions_batch([tx.model_dump() for tx in parsed_transactions])

        return parsed_transactions

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))