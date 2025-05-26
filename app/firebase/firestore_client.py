import asyncio
from datetime import datetime
from app.firebase.init import firestore
from app.schemas.transactions_schema import TransactionSchema
from google.cloud import firestore as gcf_firestore
from typing import List

db = firestore.client()

def _save_transactions_batch_sync(transactions: list):
    batch = db.batch()
    from app.services.alert_service import check_alert_conditions

    for tx in transactions:
        doc_ref = db.collection("transactions").document(tx["hash"])
        batch.set(doc_ref, tx)

        # 🔁 Guardar también en subcolección del usuario (si se conoce)
        if tx.get("user_id"):
            user_tx_ref = (
                db.collection("users")
                .document(tx["user_id"])
                .collection("transactions")
                .document(tx["hash"])
            )
            batch.set(user_tx_ref, tx)

        check_alert_conditions(tx)

    batch.commit()
async def save_transactions_batch(transactions: list):
    await asyncio.to_thread(_save_transactions_batch_sync, transactions)

def save_analyzed_transaction(data: dict):
    data["analysis_timestamp"] = datetime.utcnow().isoformat()
    data["real_label"] = None
    doc_ref = db.collection("analyzed_transactions").document()
    doc_ref.set(data)

async def get_transactions_by_wallet(wallet_address: str, limit: int = 10) -> List[TransactionSchema]:
    try:
        query = (
            db.collection_group("transactions")
            .where("from_address", "==", wallet_address)
            .order_by("timestamp", direction=gcf_firestore.Query.DESCENDING)
            .limit(limit)
        )
        results = query.stream()
        transactions = []

        for doc in results:  # `collection_group.stream()` no requiere `async for`
            tx_dict = doc.to_dict()
            tx_dict["hash"] = doc.id  # Añade el ID si es necesario
            transactions.append(TransactionSchema(**tx_dict))

        return transactions

    except Exception as e:
        print(f"❌ Error en get_transactions_by_wallet: {e}")
        return []
