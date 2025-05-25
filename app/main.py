from fastapi import FastAPI
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from app.core import config
# Add JWT bearer authentication to the OpenAPI docs
from fastapi.openapi.models import SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from app.api.v1.routers.ml_router import router as ml_router
from app.api.v1.routers.transactions_router import router as transactions_router
from app.api.v1.routers.health_router import router as health_router
from app.api.v1.routers.alerts_router import router as alerts_router
from app.api.v1.routers.analyze_router import router as analyze_router
from app.api.v1.routers.risks_router import router as risks_router
from app.api.v1.routers.admin_register_router import router as admin_register_router
from app.api.v1.routers.label_router import router as label_router
from app.api.v1.routers.user_router import router as user_router


app = FastAPI(
    title="ChainSentinel API",
    description="Blockchain fraud detection system with ML",
    version="1.0.0",
    openapi_tags=[
        {"name": "analyze", "description": "Transaction analysis"},
        {"name": "alerts", "description": "Alert system"},
        {"name": "labels", "description": "Admin label correction"},
        {"name": "ml", "description": "Machine Learning operations"},
    ],
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": True}
)

app.include_router(transactions_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(analyze_router, prefix="/api/v1")
app.include_router(risks_router, prefix="/api/v1")
app.include_router(ml_router, prefix="/api/v1")
app.include_router(admin_register_router, prefix="/api/v1")
app.include_router(label_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "ChainSentinel API running!"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ChainSentinel API",
        version="1.0.0",
        description="API for Blockchain Transaction Fraud Detection",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
