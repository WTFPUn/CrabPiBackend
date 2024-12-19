from dotenv import load_dotenv
import os
from logger import logger

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
HARDWARE_DEV_MODE=True if os.getenv("HARDWARE_DEV_MODE", "True").lower() == "true" else False
DETECTION_DEV_MODE=True if os.getenv("DETECTION_DEV_MODE", "True").lower() == "true" else False
API_DEV_MODE=True if os.getenv("API_DEV_MODE", "True").lower() == "true" else False
CAPTURE_DEV_MODE=True if os.getenv("CAPTURE_DEV_MODE", "True").lower() == "true" else False
AUTO_SHIFT_Y = int(os.getenv("AUTO_SHIFT_Y", 5))
ROW_BOX = int(os.getenv("ROW_BOX", 2))
COL_BOX = int(os.getenv("COL_BOX", 2))
CAM_SHIFT_TIME = float(os.getenv("CAM_SHIFT_TIME", 5))
RAFT_SHIFT_TIME = float(os.getenv("RAFT_SHIFT_TIME", 5))

logger.info("Configuration loaded.")
logger.info(f"SHIFT_INTERVAL: {SHIFT_INTERVAL}")
logger.info(f"MODEL_PATH: {MODEL_PATH}")
logger.info(f"CREDENTIAL: {CREDENTIAL}")
logger.info(f"BACKEND_URL: {BACKEND_URL}")
logger.info(f"CAMERA_URL: {CAMERA_URL}")
logger.info(f"X_AXIS_PIN: {X_AXIS_PIN}")
logger.info(f"Y_AXIS_PIN: {Y_AXIS_PIN}")
logger.info(f"HARDWARE_DEV_MODE: {HARDWARE_DEV_MODE}")
logger.info(f"DETECTION_DEV_MODE: {DETECTION_DEV_MODE}")
logger.info(f"API_DEV_MODE: {API_DEV_MODE}")
logger.info(f"CAPTURE_DEV_MODE: {CAPTURE_DEV_MODE}")
logger.info(f"AUTO_SHIFT_Y: {AUTO_SHIFT_Y}")
logger.info(f"ROW_BOX: {ROW_BOX}")
logger.info(f"COL_BOX: {COL_BOX}")
