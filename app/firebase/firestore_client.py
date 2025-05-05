import os
import json
import base64
import asyncio

from google.cloud import firestore
from google.oauth2 import service_account
from app.core.config import settings

def get_firestore_credentials():
    # Try loading from FIREBASE_CREDENTIALS_JSON
    firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if firebase_json:
        try:
            decoded = base64.b64decode(firebase_json)
            cred_dict = json.loads(decoded)
            return service_account.Credentials.from_service_account_info(cred_dict)
        except Exception as e:
            raise RuntimeError(f"Error loading FIREBASE_CREDENTIALS_JSON: {e}")

    # Fallback to FIREBASE_CREDENTIALS file path
    firebase_path = getattr(settings, "FIREBASE_CREDENTIALS", None)
    if firebase_path:
        try:
            return service_account.Credentials.from_service_account_file(firebase_path)
        except Exception as e:
            raise RuntimeError(f"Error loading FIREBASE_CREDENTIALS file: {e}")

    raise RuntimeError("No Firebase credentials provided via JSON or file path.")


credentials = get_firestore_credentials()

# Create Firestore client
db = firestore.Client(credentials=credentials)

def _save_transactions_batch_sync(transactions: list):
    batch = db.batch()
    for tx in transactions:
        doc_ref = db.collection("transactions").document(tx["hash"])
        batch.set(doc_ref, tx)
    batch.commit()

# Save transactions in batch
async def save_transactions_batch(transactions: list):
    await asyncio.to_thread(_save_transactions_batch_sync, transactions)
# Save a single tra