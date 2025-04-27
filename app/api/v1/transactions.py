from fastapi import APIRouter, HTTPException
from typing import List
from app.services.blockchain_service import get_transactions_by_address
from app.models.transactions import Transaction
from app.firebase.firestore_client import save_transaction

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)

# Transactions API routes
@router.get("/{address}", response_model=List[Transaction])
async def list_transactions(address: str):
    try:
        transactions = await get_transactions_by_address(address)

        parsed_transactions = []
        for tx in transactions:
            transaction_data = {
                "blockNumber": tx.get("blockNumber"),
                "timeStamp": tx.get("timeStamp"),
                "hash": tx.get("hash"),
                "nonce": tx.get("nonce"),
                "blockHash": tx.get("blockHash"),
                "transactionIndex": tx.get("transactionIndex"),
                "from_address": tx.get("from"),
                "to_address": tx.get("to"),
                "value": tx.get("value"),
                "gas": tx.get("gas"),
                "gasPrice": tx.get("gasPrice"),
                "isError": tx.get("isError"),
                "txreceipt_status": tx.get("txreceipt_status"),
                "contractAddress": tx.get("contractAddress"),
                "cumulativeGasUsed": tx.get("cumulativeGasUsed"),
                "gasUsed": tx.get("gasUsed"),
                "confirmations": tx.get("confirmations"),
                "methodId": tx.get("methodId"),
                "functionName": tx.get("functionName"),
            }
            parsed_transactions.append(transaction_data)

            # Save every transaction in Firestore
            save_transaction(transaction_data)

        return parsed_transactions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))