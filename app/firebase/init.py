import json
import base64
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials, initialize_app, firestore as firebase_firestore
from app.core.config import settings

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    firebase_json = settings.FIREBASE_CREDENTIALS_JSON
    firebase_path = settings.FIREBASE_CREDENTIALS

    firebase_cred = None

    if firebase_json:
        try:
            decoded = base64.b64decode(firebase_json)
            cred_dict = json.loads(decoded)
            firebase_cred = credentials.Certificate(cred_dict)
        except Exception as e:
            raise RuntimeError(f"Error decoding FIREBASE_CREDENTIALS_JSON: {e}")
    elif firebase_path:
        try:
            firebase_cred = credentials.Certificate(firebase_path)
        except Exception as e:
            raise RuntimeError(f"Error loading FIREBASE_CREDENTIALS from file: {e}")

    if not firebase_cred:
        raise RuntimeError("No Firebase credentials provided.")

    initialize_app(firebase_cred)

# Exportar módulos ya inicializados
auth = firebase_auth
firestore = firebase_firestore
