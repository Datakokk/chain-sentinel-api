from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    FIREBASE_CREDENTIALS_JSON = os.getenv("FIREBASE_CREDENTIALS_JSON")
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
    ETHERSCAN_API_URL: str = "https://api.etherscan.io/api"
    ML_SERVICE_URL = os.getenv("ML_SERVICE_URL")

settings = Settings()