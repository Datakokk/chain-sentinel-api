import asyncio
from app.firebase.init import firestore  

# Crear cliente Firestore
db = firestore.client()

def _save_transactions_batch_sync(transactions: list):
    """
    Guarda un lote de transacciones en Firestore de forma síncrona.
    """
    batch = db.batch()
    from app.services.alert_service import check_alert_conditions

    for tx in transactions:
        doc_ref = db.collection("transactions").document(tx["hash"])
        batch.set(doc_ref, tx)
        check_alert_conditions(tx)
    batch.commit()


async def save_transactions_batch(transactions: list):
    """
    Guarda un lote de transacciones de forma asíncrona usando threading.
    """
    await asyncio.to_thread(_save_transactions_batch_sync, transactions)

from firebase_admin import auth
from app.firebase.init import firestore  # usa la instancia compartida

# Instancia del cliente
db = firestore.client()

async def verify_admin_token(token: str) -> dict:
    """
    Verifica si el token pertenece a un usuario administrador.

    Args:
        token (str): Firebase JWT

    Returns:
        dict: El token decodificado si es válido y es admin.

    Raises:
        HTTPException: Si el token no es válido o el usuario no es admin.
    """
    from fastapi import HTTPException

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]

        doc_ref = db.collection("users").document(uid)
        doc = doc_ref.get()

        if doc.exists and doc.to_dict().get("admin", False):
            return decoded_token
        else:
            raise HTTPException(status_code=403, detail="No tienes permiso de administrador.")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")
