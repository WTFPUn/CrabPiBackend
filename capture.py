import asyncio
import numpy as np
from logger import logger


async def capture_images(image_queue: asyncio.Queue):
    """
    Coroutine that captures images and puts them into the queue.
    """
    while True:
        # Simulate image capture
        image = np.zeros(
            (480, 640, 3), dtype=np.uint8
        )  # Placeholder for an image frame
        logger.info("Captured image and put into queue.")
        await image_queue.put(image)

        await asyncio.sleep(1)  # Adjust the delay as needed
