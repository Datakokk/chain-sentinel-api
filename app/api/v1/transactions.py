from fastapi import APIRouter

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)

# Test route
@router.get("/")
async def list_transactions():
    return {"message": "Here you will see the list of transactions."}