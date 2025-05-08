from datetime import datetime
from typing import Optional
from app.firebase.firestore_client import db

UMBRAL_VALOR = 10000
SUSPICIOUS_COLLECTION = "suspicious_addresses"
ALERTS_COLLECTION = "alerts"

def check_alert_conditions(transaction: dict, user_id: Optional[str] = None):
    from_address = transaction.get("from_address")
    to_address = transaction.get("to_address")
    value = transaction.get("value")

    triggered_alerts = []

    if value and float(value) > UMBRAL_VALOR:
        triggered_alerts.append({
            "type": "high_value",
            "message": f"Transacción de valor alto detectada: {value}",
            "severity": "critical"
        })

    suspicious_addresses = db.collection(SUSPICIOUS_COLLECTION).stream()
    suspicious_set = {doc.id for doc in suspicious_addresses}

    if from_address in suspicious_set or to_address in suspicious_set:
        triggered_alerts.append({
            "type": "suspicious_address",
            "message": "Dirección sospechosa detectada en la transacción",
            "severity": "warning"
        })

    for alert in triggered_alerts:
        alert_doc = {
            "transaction_hash": transaction.get("hash"),
            "from_address": from_address,
            "to_address": to_address,
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "type": alert["type"],
            "message": alert["message"],
            "severity": alert["severity"],
            "user_id": user_id  # <- Esto es lo que permite luego filtrar
        }
        db.collection(ALERTS_COLLECTION).add(alert_doc)

    return triggered_alerts
