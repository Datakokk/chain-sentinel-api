from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.firebase.init import auth, firestore 

security = HTTPBearer()
db = firestore.client()

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

async def verify_admin_token(token: str) -> dict:
    """
    Verifies if the token belongs to an admin user.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]

        doc_ref = db.collection("users").document(uid)
        doc = doc_ref.get()

        if doc.exists and doc.to_dict().get("admin", False):
            return decoded_token
        else:
            raise HTTPException(status_code=403, detail="You are not an admin.")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
