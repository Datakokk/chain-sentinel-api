from fastapi import APIRouter
from google.cloud import firestore
from google.oauth2 import service_account
from app.core.config import settings
import os
import json
import base64

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    errors = []

    # Verificar ETHERSCAN_API_KEY
    etherscan_key = os.getenv("ETHERSCAN_API_KEY")
    if not etherscan_key:
        errors.append("ETHERSCAN_API_KEY no está definida.")

    # Verificar Firestore con mismo método que en firestore_client.py
    try:
        if settings.ENVIRONMENT == "production":
            firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
            decoded = base64.b64decode(firebase_json)
            cred_dict = json.loads(decoded)
            credentials = service_account.Credentials.from_service_account_info(cred_dict)
        else:
            credentials = service_account.Credentials.from_service_account_file(settings.FIREBASE_CREDENTIALS)

        db = firestore.Client(credentials=credentials)
        _ = list(db.collection("transactions").limit(1).stream())
    except Exception as e:
        errors.append(f"Error al conectar con Firestore: {str(e)}")

    if errors:
        return {"status": "fail", "errors": errors}

    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "message": "Firestore y Etherscan configurados correctamente"
    }
