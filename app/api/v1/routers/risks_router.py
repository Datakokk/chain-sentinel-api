from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import datetime
from datetime import timezone
from app.auth.firebase_auth import verify_token
from app.firebase.firestore_client import db

router = APIRouter(prefix="/risks", tags=["risks"])

@router.get("")
def get_suspicious_transactions(
    user_data: dict = Depends(verify_token),
    start_date: Optional[datetime] = Query(None, description="Filtrar desde esta fecha"),
    end_date: Optional[datetime] = Query(None, description="Filtrar hasta esta fecha")
):
    """
    Returns suspicious transactions:
    - is_fraud == True
    - or risk_score > 0.9
    - Optionally filtered by date range.
    - Expanded with transaction data.
    """
    collection = db.collection("transaction_analyses")

    # 1. Separate queries
    query_fraud = collection.where("is_fraud", "==", True).stream()
    query_risk = collection.where("risk_score", ">", 0.9).stream()

    # 2. Merge without duplicates
    combined = {}
    for doc in list(query_fraud) + list(query_risk):
        data = doc.to_dict()
        doc_id = doc.id
        analyzed_at = data.get("analyzed_at")
        if isinstance(analyzed_at, str):
            analyzed_at = datetime.fromisoformat(analyzed_at.replace("Z", "+00:00"))
        if analyzed_at:
            # Filter by date if specified
            # Asegura que ambas fechas tengan zona horaria UTC
            if analyzed_at and analyzed_at.tzinfo is None:
                analyzed_at = analyzed_at.replace(tzinfo=timezone.utc)
            if start_date and start_date.tzinfo is None:
                start_date = start_date.replace(tzinfo=timezone.utc)
            if end_date and end_date.tzinfo is None:
                end_date = end_date.replace(tzinfo=timezone.utc)
            
            # Ahora puedes comparar sin errores
            if start_date and analyzed_at < start_date:
                continue
            if end_date and analyzed_at > end_date:
                continue
        data["analyzed_at"] = analyzed_at
        data["id"] = doc_id
        combined[doc_id] = data

    # 3. Add related transaction data
    enriched = []
    for item in combined.values():
        tx_id = str(item.get("id_transaccion"))
        tx_doc = db.collection("transactions").document(tx_id).get()
        if tx_doc.exists:
            item["transaction"] = tx_doc.to_dict()
        else:
            item["transaction"] = None
        enriched.append(item)

    # 4. Sort and limit
    sorted_results = sorted(
        enriched,
        key=lambda d: d.get("analyzed_at") or datetime.min,
        reverse=True
    )

    return sorted_results[:20]
