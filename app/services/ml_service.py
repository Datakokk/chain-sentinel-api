import os
# import httpx

import asyncio
from random import random

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL")  # e.g. https://ml-service-xxxxx.a.run.app

# async def analyze_transaction_ml(payload: dict) -> dict:
#     async with httpx.AsyncClient(timeout=10.0) as client:
#         resp = await client.post(f"{ML_SERVICE_URL}/predict", json=payload)
#         resp.raise_for_status()
#         return resp.json()

async def analyze_transaction_ml(payload: dict) -> dict:
    # Simulate a machine learning model prediction
    await asyncio.sleep(0.1)  # Simulate network delay  
    # Simulate a random prediction
    return {
        "is_fraud": random() < 0.5,  # Randomly classify as fraud or not
        "risk_score": round(random(), 4),  # Random risk score between 0 and 1
    }