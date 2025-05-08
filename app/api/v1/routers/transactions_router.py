from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.blockchain_service import get_transactions_by_address
from app.firebase.firestore_client import save_transactions_batch
from app.schemas.transactions_schema import TransactionSchema, TransactionCreateSchema
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

@router.post("", tags=["transactions"])
async def create_transaction(tx: TransactionCreateSchema):
    """
    Crea una nueva transacción y evalúa condiciones de alerta.
    """
    try:
        tx_dict = tx.model_dump()
        await save_transactions_batch([tx_dict])  # llamamos a la función asíncrona
        return {"message": "Transacción guardada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar transacción: {str(e)}")