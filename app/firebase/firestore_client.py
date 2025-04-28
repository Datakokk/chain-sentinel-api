from google.cloud import firestore
from google.oauth2 import service_account
from app.core.config import settings

firestore_cred = service_account.Credentials.from_service_account_file(
    settings.FIREBASE_CREDENTIALS
)

db = firestore.Client(credentials=firestore_cred)

async def save_transactions_batch(transactions: list):
    batch = db.batch()

    for tx in transactions:
        doc_ref = db.collection("transactions").document(tx["hash"])
        batch.set(doc_ref, tx)

    batch.commit()