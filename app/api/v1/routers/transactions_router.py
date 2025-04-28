from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.blockchain_service import get_transactions_by_address
from app.firebase.firestore_client import save_transactions_batch
from app.schemas.transactions_schema import TransactionSchema

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/{address}", response_model=List[TransactionSchema])
async def list_transactions(address: str, limit: int = Query(10, ge=1, le=100)):
    try:
        transactions = await get_transactions_by_address(address)
        transactions = transactions[:limit]

        parsed_transactions = []
        for tx in transactions:
            transaction_data = {
                "hash": tx.get("hash"),
                "from_address": tx.get("from"),
                "to_address": tx.get("to"),
                "value": int(tx.get("value")),
                "timestamp": tx.get("timeStamp"),
            }
            parsed_transactions.append(transaction_data)

        await save_transactions_batch(parsed_transactions)

        return parsed_transactions  # 🔥 devolvemos los parseados, no los originales
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
