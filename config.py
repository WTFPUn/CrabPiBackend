from dotenv import load_dotenv
import os

load_dotenv()

# Access TIME_INTERVAL from .env
SHIFT_INTERVAL = int(os.getenv("TIME_INTERVAL", 5))  # Default to 5 seconds if not set
MODEL_PATH = os.getenv("MODEL_PATH", "best.pt")
CREDENTIAL = os.getenv("CREDENTIAL", "my_credential")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")
