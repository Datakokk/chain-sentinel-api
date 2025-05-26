from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.blockchain_service import get_transactions_by_address
from app.firebase.firestore_client import save_transactions_batch
from app.schemas.transactions_schema import TransactionSchema, TransactionCreateSchema

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/{address}", response_model=List[TransactionSchema])
async def list_transactions(address: str, limit: int = Query(10, ge=1, le=100)):
    try:
        # Obtener transacciones (ej. desde Etherscan)
        transactions = await get_transactions_by_address(address)
        transactions = transactions[:limit]

        normalized = []

        for tx in transactions:
            normalized_tx = {
                "hash": tx.hash,
                "from_address": getattr(tx, "from", tx.from_address),  # compatible con alias si viene de Etherscan
                "to_address": getattr(tx, "to", tx.to_address),
                "value": float(tx.value),
                "timestamp": int(tx.timeStamp if hasattr(tx, "timeStamp") else tx.timestamp),
                "user_id": None,
                "status": "pending",
                "analysis_id": None
            }
            normalized.append(normalized_tx)

        # Guardar en Firestore
        await save_transactions_batch(normalized)

        # Devolver al frontend
        return normalized

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", tags=["transactions"])
async def create_transaction(tx: TransactionCreateSchema):
    """
    Crea una nueva transacción y la guarda en Firestore.
    """
    try:
        tx_dict = tx.model_dump()
        await save_transactions_batch([tx_dict])
        return {"message": "Transacción guardada correctamente", "transaction": tx_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar transacción: {str(e)}")
