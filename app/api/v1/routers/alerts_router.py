# routes/alerts.py

from fastapi import APIRouter, Depends
from app.auth.firebase_auth import verify_token

router = APIRouter()

@router.get("/alerts")
def get_alerts(user_data: dict = Depends(verify_token)):
    uid = user_data["uid"]  # Extract the authenticated user's ID

    # Simulation: example alerts (later we will connect with Firestore or DB)
    fake_alerts = [
        {"id": 1, "mensaje": "Transacción sospechosa detectada", "tipo": "critical", "user_id": uid},
        {"id": 2, "mensaje": "Límite de umbral superado", "tipo": "warning", "user_id": uid}
    ]

    return {"alerts": fake_alerts}
