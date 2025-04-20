from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import transactions

app = FastAPI(
    title="chain-sentinel-api",
    description="API for fraud detection in blockchain transactions",
    version="0.1.0",   
)

# Configure CORS (we can restrict this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(transactions.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Chain Sentinel API!"}