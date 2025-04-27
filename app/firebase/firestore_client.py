import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def save_transaction(transaction: dict):
    """
    Save a transaction document into the Firestore 'transactions' collection.
    """
    transaction_ref = db.collection("transactions").document(transaction["hash"])
    transaction_ref.set(transaction)
