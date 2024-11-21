from dotenv import load_dotenv
import os

load_dotenv()

# Access TIME_INTERVAL from .env
SHIFT_INTERVAL = int(os.getenv("TIME_INTERVAL", 5))  # Default to 5 seconds if not set
MODEL_PATH = os.getenv("MODEL_PATH", "best.pt")
CREDENTIAL = os.getenv("CREDENTIAL", "my_credential")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")
CAMERA_URL = os.getenv("CAMERA_URL", "http://localhost:8000/camera")
# Y is referred to as the long axis, X is the short axis
X_AXIS_PIN = int(os.getenv("X_AXIS_PIN", 17))
Y_AXIS_PIN = int(os.getenv("Y_AXIS_PIN", 18))
X_STEP = int(os.getenv("X_STEP", 4))
Y_STEP = int(os.getenv("Y_STEP", 10))
DEV_MODE = bool(os.getenv("DEV_MODE", False))
AUTO_SHIFT_Y = int(os.getenv("AUTO_SHIFT_Y", 5))
ROW_BOX = int(os.getenv("ROW_BOX", 2))
COL_BOX = int(os.getenv("COL_BOX", 2))