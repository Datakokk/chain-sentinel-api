from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import firestore

router = APIRouter(prefix="/auth", tags=["Admin Registration"])
db = firestore.client()

class AdminRegisterPayload(BaseModel):
    uid: str
    email: str

@router.post("/register-admin")
async def register_admin(payload: AdminRegisterPayload):
    try:
        doc_ref = db.collection("users").document(payload.uid)
        doc_ref.set({
            "email": payload.email,
            "admin": True
        })
        return {"message": f"Usuario {payload.email} registrado como administrador."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
