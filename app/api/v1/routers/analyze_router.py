# app/api/v1/routers/analyze.py
from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.schemas.analyze_schema import TransactionAnalyzeRequest, TransactionAnalyzeResponse
from app.services.ml_service import analyze_transaction_ml
from app.firebase.firestore_client import save_analyzed_transaction, db
 
router = APIRouter(tags=["analyze"])



@router.post("/analyze", response_model=TransactionAnalyzeResponse)
async def analyze_transaction(tx: TransactionAnalyzeRequest):
    """
    Recibe una transacción, la envía al microservicio de ML
    y guarda el resultado en Firestore.
    """
    # 1) Envía los datos brutos al ML
    try:
        ml_resp = await analyze_transaction_ml(tx.dict(by_alias=True))
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error al contactar con el ML service: {e}"
        )

    # 2) Monta el documento de resultado
    analysis = {
        "id_transaccion": tx.id_transaccion,
        "is_fraud":    ml_resp.get("is_fraud", False),
        "risk_score":  ml_resp.get("risk_score", 0.0),
        "analyzed_at": datetime.utcnow().isoformat() + "Z"
    }

    # 3) Guarda en Firestore usando el cliente ya inicializado
    try:
        doc_ref = db.collection("transaction_analyses") \
                    .document(str(analysis["id_transaccion"]))
        doc_ref.set(analysis)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar en Firestore: {e}"
        )
    
    # 4) Save full transaction with prediction
    try:
        transaction_to_save = {
            "hash": tx.hash,
            "origin": tx.origin_address,
            "destination": tx.destination_address,
            "amount": tx.amount,
            "prediction_result": "fraud" if analysis["is_fraud"] else "not_fraud"
        }
        save_analyzed_transaction(transaction_to_save)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving full transaction to Firestore: {e}"
        )


    # 5) Devuelve al cliente la respuesta tipada
    return TransactionAnalyzeResponse(**analysis)


