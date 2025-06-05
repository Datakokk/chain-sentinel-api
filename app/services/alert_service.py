from datetime import datetime
from typing import Optional
from app.firebase.firestore_client import db

UMBRAL_VALOR = 10000
SUSPICIOUS_COLLECTION = "suspicious_addresses"

def check_alert_conditions(transaction: dict, user_id: Optional[str] = None):
    from_address = (transaction.get("from_address") or "").strip().lower()
    to_address = (transaction.get("to_address") or "").strip().lower()
    value = transaction.get("value")

    print(f"[DEBUG] Revisando condiciones de alerta para usuario: {user_id}")
    print(f"[DEBUG] Transacción recibida: {transaction}")
    print(f"[DEBUG] Dirección from_address normalizada: '{from_address}'")
    print(f"[DEBUG] Dirección to_address normalizada: '{to_address}'")

    triggered_alerts = []

    # Condición de valor alto
    try:
        if value and float(value) > UMBRAL_VALOR:
            triggered_alerts.append({
                "type": "high_value",
                "message": f"Transacción de valor alto detectada: {value}",
                "severity": "critical"
            })
    except ValueError:
        print(f"[ERROR] No se pudo convertir el valor '{value}' a float.")

    # Condición de direcciones sospechosas
    suspicious_addresses = db.collection(SUSPICIOUS_COLLECTION).stream()
    suspicious_set = {doc.id.lower() for doc in suspicious_addresses}
    print("[DEBUG] Direcciones sospechosas registradas en Firestore:", suspicious_set)

    print(f"[DEBUG] Comparando from_address: {'✅' if from_address in suspicious_set else '❌'}")
    print(f"[DEBUG] Comparando to_address: {'✅' if to_address in suspicious_set else '❌'}")

    if from_address in suspicious_set or to_address in suspicious_set:
        triggered_alerts.append({
            "type": "suspicious_address",
            "message": "Dirección sospechosa detectada en la transacción",
            "severity": "warning"
        })

    if not triggered_alerts:
        print("[DEBUG] La transacción fue procesada pero no se generaron alertas.")

    for alert in triggered_alerts:
        if not user_id:
            print("[ERROR] user_id es None o vacío. No se puede guardar la alerta.")
            continue

        print(f"[DEBUG] Guardando alerta para user_id={user_id} >>> {alert}")

        try:
            user_ref = db.collection("users").document(user_id)
            user_snapshot = user_ref.get()
            if not user_snapshot.exists:
                print(f"[WARNING] El documento users/{user_id} NO existe en Firestore")
                continue
            else:
                print(f"[DEBUG] El documento users/{user_id} existe correctamente")

            alert_doc = {
                "transaction_hash": transaction.get("hash"),
                "from_address": from_address,
                "to_address": to_address,
                "value": value,
                "timestamp": datetime.utcnow().isoformat(),
                "type": alert["type"],
                "message": alert["message"],
                "severity": alert["severity"],
                "user_id": user_id
            }

            print(f"[DEBUG] Guardando alerta en users/{user_id}/alerts: {alert_doc}")
            user_ref.collection("alerts").add(alert_doc)
            print(f"[DEBUG] Alerta guardada correctamente en alerts/")
        except Exception as e:
            print(f"[ERROR] No se pudo guardar la alerta en Firestore: {e}")

    print(f"[DEBUG] Total de alertas generadas: {len(triggered_alerts)}")
    return triggered_alerts
