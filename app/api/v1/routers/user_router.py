from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.auth.firebase_auth import verify_token
from app.firebase.init import firestore


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/me", summary="Get current authenticated user")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    user_id = credentials["uid"]
    doc_ref = firestore.collection("users").document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        return {"error": "Usuario no encontrado"}

    user_data = doc.to_dict()
    user_data["id"] = user_id
    return user_data
