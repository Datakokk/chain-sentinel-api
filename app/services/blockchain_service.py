from app.core.config import settings
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
            data = response.json()

            if data["status"] != "1":
                raise ValueError(f"Etherscan error: {data.get('message')}")

            if not isinstance(data["result"], list):
                raise ValueError("Unexpected response format from Etherscan.")

            return data["result"]

        except httpx.RequestError as e:
            raise ValueError(f"Network error: {str(e)}")
