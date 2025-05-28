from fastapi import APIRouter, Depends, Query, Body, HTTPException, status
from datetime import datetime
from typing import Optional

from app.schemas.alert_schema import AlertCreate
from app.auth.firebase_auth import verify_token
from app.firebase.firestore_client import db

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("")
def get_alerts_by_user(user_data: dict = Depends(verify_token)):
    """
    Devuelve alertas desde la subcolección del usuario autenticado.
    """
    uid = user_data["uid"]
    alerts_ref = db.collection("users").document(uid).collection("alerts").stream()
    return [doc.to_dict() | {"id": doc.id} for doc in alerts_ref]


@router.get("/by-address")
def get_alerts_by_address(
    address: Optional[str] = Query(None, description="Dirección de origen o destino"),
    user_data: dict = Depends(verify_token)
):
    """
    Devuelve alertas por dirección, solo dentro del usuario autenticado.
    """
    uid = user_data["uid"]
    alerts_ref = db.collection("users").document(uid).collection("alerts")

    if address:
        query_from = alerts_ref.where("from_address", "==", address).stream()
        query_to = alerts_ref.where("to_address", "==", address).stream()
        results = list(query_from) + list(query_to)
    else:
        results = alerts_ref.stream()

    return [doc.to_dict() | {"id": doc.id} for doc in results]


@router.post("")
def create_alert(
    alert: AlertCreate = Body(...),
    user_data: dict = Depends(verify_token)
):
    """
    Crea una alerta dentro del usuario autenticado.
    """
    uid = user_data["uid"]
    data = alert.dict()
    data["user_id"] = uid
    data["created_at"] = data.get("created_at") or datetime.utcnow()

    doc_ref = db.collection("users").document(uid).collection("alerts").add(data)
    alert_id = doc_ref[1].id  # Firestore devuelve (write_result, reference)
    return {
        "message": "Alerta creada correctamente",
        "alert_id": alert_id,
        "data": data
    }


@router.delete("/{alert_id}")
def delete_alert(
    alert_id: str,
    user_data: dict = Depends(verify_token)
):
    """
    Elimina una alerta por ID, solo si pertenece al usuario autenticado.
    """
    uid = user_data["uid"]
    alert_ref = db.collection("users").document(uid).collection("alerts").document(alert_id)
    alert = alert_ref.get()

    if not alert.exists:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")

    alert_ref.delete()
    return {"message": "Alerta eliminada correctamente", "alert_id": alert_id}
