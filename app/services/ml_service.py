import httpx
from typing import Any, Dict
from app.core.config import settings

import asyncio
from random import random

ML_SERVICE_URL = settings.ML_SERVICE_URL  # e.g. https://ml-service-xxxxx.a.run.app
if not ML_SERVICE_URL:
    raise RuntimeError("Missing ML_SERVICE_URL environment variable")

async def analyze_transaction_ml(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Si payload["date"] es datetime, lo pasamos a ISO-string
    ts = payload["date"]
    if hasattr(ts, "isoformat"):
        ts = ts.isoformat()

    ml_payload = {
        "amount":              payload["amount"],              # o payload["count"] según tu esquema
        "origin_address":      payload["origin_address"],      # alinea nombres
        "destination_address": payload["destination_address"],
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(f"{ML_SERVICE_URL}/predict", json=ml_payload)
        resp.raise_for_status()
        return resp.json()
    
def train_model():
    # Here goes your real training logic, for now we simulate
    try:
        # Example: load data, train and save the model
        print("Iniciando entrenamiento del modelo ML...")
        # Training simulation
        import time
        time.sleep(3)
        print("Entrenamiento finalizado.")
        return {"status": "success", "message": "Modelo entrenado correctamente."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# async def analyze_transaction_ml(payload: dict) -> dict:
#     # Simulate a machine learning model prediction
#     await asyncio.sleep(0.1)  # Simulate network delay  
#     # Simulate a random prediction
#     return {
#         "is_fraud": random() < 0.5,  # Randomly classify as fraud or not
#         "risk_score": round(random(), 4),  # Random risk score between 0 and 1
#     }