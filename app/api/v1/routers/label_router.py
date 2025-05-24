from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.firebase.firestore_client import db
from app.auth.firebase_auth import verify_admin_token

router = APIRouter(tags=["labels"])
security = HTTPBearer()

class LabelUpdateRequest(BaseModel):
    real_label: str  # Expected: "fraud" or "not_fraud"

@router.patch("/transactions/{doc_id}/label")
async def update_real_label(
    doc_id: str,
    payload: LabelUpdateRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Allows an admin to update the real_label of an analyzed transaction.
    Requires JWT Bearer token (use Swagger 'Authorize' button).
    """
    token = credentials.credentials
    await verify_admin_token(token)

    try:
        doc_ref = db.collection("analyzed_transactions").document(doc_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Transaction not found")

        doc_ref.update({"real_label": payload.real_label})
        return {
            "message": "real_label updated",
            "real_label": payload.real_label
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update real_label: {e}")
