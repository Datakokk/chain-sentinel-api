import asyncio
from app.firebase.init import firestore  # 👈 Reutiliza la instancia centralizada

# Crear cliente Firestore
db = firestore.client()

def _save_transactions_batch_sync(transactions: list):
    """
    Guarda un lote de transacciones en Firestore de forma síncrona.
    """
    batch = db.batch()
    for tx in transactions:
        doc_ref = db.collection("transactions").document(tx["hash"])
        batch.set(doc_ref, tx)
    batch.commit()


async def save_transactions_batch(transactions: list):
    """
    Guarda un lote de transacciones de forma asíncrona usando threading.
    """
    await asyncio.to_thread(_save_transactions_batch_sync, transactions)
