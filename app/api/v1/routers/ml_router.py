from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.firebase.firestore_client import verify_admin_token
from app.services.ml_service import train_model
from app.core.config import settings
import httpx

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

security = HTTPBearer()

@router.post("/train")
async def train_ml_model(token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Entrena el modelo ML. Requiere que el usuario sea administrador.
    """
    await verify_admin_token(token.credentials)
    result = train_model()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.get("/train/status")
async def get_model_status(token: HTTPAuthorizationCredentials = Depends(security)):
    await verify_admin_token(token.credentials)

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.ML_SERVICE_URL}/status")
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo consultar el estado del modelo: {e}")