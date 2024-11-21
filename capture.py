import asyncio
import numpy as np
from logger import logger
from config import CAPTURE_DEV_MODE, SHIFT_INTERVAL, CAMERA_URL, HARDWARE_DEV_MODE
import time
import cv2
from processing import force_shift_camera
import random
import os

choice = os.listdir("imgs")


if not CAPTURE_DEV_MODE:
    camera = cv2.VideoCapture(CAMERA_URL)


async def capture_images(image_queue: asyncio.Queue):
    """
    Coroutine that captures images and puts them into the queue.
    """
    while True:
        # Simulate image capture
        start_time = time.time()
        if not CAPTURE_DEV_MODE:
            ret, image = camera.read()
            if not ret:
                logger.error("Failed to capture image.")
                continue
        else:
            image = cv2.imread(f"imgs/{random.choice(choice)}")
            logger.info("Captured image and put into queue.")
        await image_queue.put(image)
        end = time.time()

        await asyncio.sleep(SHIFT_INTERVAL - (end - start_time) if SHIFT_INTERVAL - (end - start_time) > 0 else 0)
        if  HARDWARE_DEV_MODE:
            await force_shift_camera()
