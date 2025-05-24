import asyncio
from datetime import datetime
from app.firebase.init import firestore

db = firestore.client()

def _save_transactions_batch_sync(transactions: list):
    batch = db.batch()
    from app.services.alert_service import check_alert_conditions

    for tx in transactions:
        doc_ref = db.collection("transactions").document(tx["hash"])
        batch.set(doc_ref, tx)
        check_alert_conditions(tx)
    batch.commit()

async def save_transactions_batch(transactions: list):
    await asyncio.to_thread(_save_transactions_batch_sync, transactions)

def save_analyzed_transaction(data: dict):
    data["analysis_timestamp"] = datetime.utcnow().isoformat()
    data["real_label"] = None
    doc_ref = db.collection("analyzed_transactions").document()
    doc_ref.set(data)
