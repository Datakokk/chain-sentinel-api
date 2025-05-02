from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials, initialize_app
import firebase_admin
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la ruta desde la variable de entorno
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")

# Inicializar Firebase si no está ya iniciado
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_path)
    initialize_app(cred)

# Middleware-like dependency
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
