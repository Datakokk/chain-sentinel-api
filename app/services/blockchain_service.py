from app.core.config import settings
from app.schemas.etherscan_schema import EtherscanResponse
import httpx


async def get_transactions_by_address(address: str):
    """Get transaction list from Etherscan by wallet address."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": settings.ETHERSCAN_API_KEY,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(settings.ETHERSCAN_API_URL, params=params)
            response.raise_for_status()

            print("DEBUG RAW JSON:", response.json())
            # Validate and parse the response with Pydantic
            data = EtherscanResponse(**response.json())

            if data.status != "1":
                raise ValueError(f"Etherscan error: {data.message}")

            return data.result  # EtherscanTransaction list

        except httpx.RequestError as e:
            raise ValueError(f"Network error: {str(e)}")
        except Exception as e:
            print("DEBUG Exception:", e)  
            raise ValueError(f"Unexpected error: {str(e)}")
