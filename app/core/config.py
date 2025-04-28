from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
    ETHERSCAN_API_URL: str = "https://api.etherscan.io/api"

settings = Settings()