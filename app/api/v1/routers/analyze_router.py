# app/api/v1/routers/analyze.py
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from app.schemas.analyze_schema import TransactionAnalyzeRequest, TransactionAnalyzeResponse
from app.services.ml_service import analyze_transaction_ml
from app.auth.firebase_auth import verify_token
from app.firebase.firestore_client import db

router = APIRouter(tags=["analyze"])

@router.post("/analyze", response_model=TransactionAnalyzeResponse)
async def analyze_transaction(
    tx: TransactionAnalyzeRequest,
    user_data: dict = Depends(verify_token)
):
    """
    Recibe una transacción, la envía al microservicio de ML,
    y guarda el resultado en Firestore bajo el usuario autenticado.
    """
    uid = user_data["uid"]

    # Validación de hashes maliciosos o inexistentes conocidos
    HASHES_INVALIDOS = {
        "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdf",
        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
        "0x1111111111111111111111111111111111111111111111111111111111111111",
    }

    if tx.id_transaccion.lower() in HASHES_INVALIDOS:
        raise HTTPException(
            status_code=400,
            detail="Hash inválido o no existente en la red."
        )


    # 1) Enviar los datos brutos al microservicio ML
    try:
        ml_resp = await analyze_transaction_ml(tx.dict(by_alias=True))
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error al contactar con el ML service: {e}"
        )

    # 2) Montar el documento de análisis
    analysis = {
        "id_transaccion": tx.id_transaccion,
        "is_fraud": ml_resp.get("is_fraud", False),
        "risk_score": ml_resp.get("risk_score", 0.0),
        "analyzed_at": datetime.utcnow().isoformat() + "Z"
    }

    # 3) Guardar análisis en subcolección del usuario
    try:
        db.collection("users").document(uid) \
          .collection("transaction_analyses") \
          .document(str(analysis["id_transaccion"])) \
          .set(analysis)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar análisis en Firestore: {e}"
        )

    # 4) Guardar transacción completa con resultado
    try:
        transaction_to_save = {
            "hash": tx.hash,
            "origin": tx.origin_address,
            "destination": tx.destination_address,
            "amount": tx.amount,
            "prediction_result": "fraud" if analysis["is_fraud"] else "not_fraud",
            "analysis_timestamp": analysis["analyzed_at"]
        }

        db.collection("users").document(uid) \
          .collection("analyzed_transactions") \
          .add(transaction_to_save)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar transacción en Firestore: {e}"
        )

    # 5) Devolver respuesta
    return TransactionAnalyzeResponse(**analysis)
