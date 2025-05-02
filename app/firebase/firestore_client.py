import os
import json
import base64
import asyncio

from google.cloud import firestore
from google.oauth2 import service_account
from app.core.config import settings

# Detect if we are in production (Cloud Run)
if settings.ENVIRONMENT == "production":
    firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if not firebase_json:
        raise RuntimeError("FIREBASE_CREDENTIALS_JSON no está definida.")
    decoded = base64.b64decode(firebase_json)
    cred_dict = json.loads(decoded)
    credentials = service_account.Credentials.from_service_account_info(cred_dict)
else:
    credentials = service_account.Credentials.from_service_account_file(settings.FIREBASE_CREDENTIALS)

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