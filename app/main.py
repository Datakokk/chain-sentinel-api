from fastapi import FastAPI
from app.core import config
from app.api.v1.routers.ml_router import router as ml_router
from app.api.v1.routers.transactions_router import router as transactions_router
from app.api.v1.routers.health_router import router as health_router
from app.api.v1.routers.alerts_router import router as alerts_router
from app.api.v1.routers.analyze_router import router as analyze_router
from app.api.v1.routers.risks_router import router as risks_router
from app.api.v1.routers.admin_register_router import router as admin_register_router

app = FastAPI(title="ChainSentinel API")

app.include_router(transactions_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(analyze_router, prefix="/api/v1")
app.include_router(risks_router, prefix="/api/v1")
app.include_router(ml_router, prefix="/api/v1")
app.include_router(admin_register_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "ChainSentinel API running!"}

