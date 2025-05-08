from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.auth.firebase_auth import verify_token
from app.firebase.firestore_client import db

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("")
def get_alerts_by_user(user_data: dict = Depends(verify_token)):
    """
    Devuelve alertas filtradas por el usuario autenticado (user_id).
    """
    uid = user_data["uid"]
    alerts_ref = db.collection("alerts").where("user_id", "==", uid).stream()
    return [doc.to_dict() for doc in alerts_ref]


@router.get("/by-address")
def get_alerts_by_address(address: Optional[str] = Query(None, description="Dirección de origen o destino")):
    """
    Devuelve alertas filtradas por dirección (from_address o to_address).
    Si no se pasa dirección, devuelve todas.
    """
    alerts_ref = db.collection("alerts")

    if address:
        query_from = alerts_ref.where("from_address", "==", address).stream()
        query_to = alerts_ref.where("to_address", "==", address).stream()
        results = list(query_from) + list(query_to)
    else:
        results = alerts_ref.stream()

    return [doc.to_dict() for doc in results]
