import asyncio
import numpy as np
from logger import logger
from config import DEV_MODE, SHIFT_INTERVAL, CAMERA_URL
import time
import cv2

if not DEV_MODE:
    camera = cv2.VideoCapture(CAMERA_URL)


async def capture_images(image_queue: asyncio.Queue):
    """
    Coroutine that captures images and puts them into the queue.
    """
    while True:
        # Simulate image capture
        start_time = time.time()
        if not DEV_MODE:
            ret, image = camera.read()
            if not ret:
                logger.error("Failed to capture image.")
                continue
        else:
            image = np.zeros(
                (480, 640, 3), dtype=np.uint8
            )  # Placeholder for an image frame
            logger.info("Captured image and put into queue.")
        await image_queue.put(image)
        end = time.time()

        await asyncio.sleep(SHIFT_INTERVAL - (end - start_time) if SHIFT_INTERVAL - (end - start_time) > 0 else 0)
