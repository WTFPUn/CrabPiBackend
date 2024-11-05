from dotenv import load_dotenv
import os

load_dotenv()

# Access TIME_INTERVAL from .env
TIME_INTERVAL = int(os.getenv("TIME_INTERVAL", 5))  # Default to 5 seconds if not set
