from fastapi import FastAPI
from app.api.v1.routers.transactions_router import router as transactions_router
from app.api.v1.routers.health_router import router as health_router
from app.api.v1.routers.alerts_router import router as alerts_router

app = FastAPI(title="ChainSentinel API")

app.include_router(transactions_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "ChainSentinel API running!"}

