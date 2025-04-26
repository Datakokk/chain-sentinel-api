import os
import httpx
from dotenv import load_dotenv

load_dotenv()  # charge .env variables

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

async def get_transactions_by_address(address: str):
    """Get transaction list from Etherscan by wallet address."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(ETHERSCAN_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "1":
            raise ValueError(f"Etherscan error: {data.get('message')}")

        return data["result"]
