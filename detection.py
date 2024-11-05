import asyncio
import random
import time
import cv2
import numpy as np
from logger import logger


async def detection_module(image_queue: asyncio.Queue, detection_queue: asyncio.Queue):
    """
    Coroutine that processes images from the image_queue,
    runs detection, and puts results into detection_queue.
    """
    while True:
        image = await image_queue.get()
        logger.info("Detection module processing image.")

        # Run detection processing
        detection_result = await run_detection_algorithm(image)

        # Put the detection result into the next queue for post-processing
        await detection_queue.put(detection_result)
        image_queue.task_done()


async def run_detection_algorithm(image):
    """
    Run detection algorithm including QR code detection.
    """
    await asyncio.sleep(0.5)  # Simulate processing time

    detections = []

    # Simulate QR code detection to get block ID
    # block_id = detect_qr_code(image)
    block_id = 1  # Placeholder for block ID

    # Simulate 'Crab' and 'Box' detections
    box_detection = {
        "class": "Box",
        "block_id": block_id,
        "bbox": [0, 0, image.shape[1], image.shape[0]],  # x, y, w, h
    }
    detections.append(box_detection)

    # Randomly decide how many crabs are in this box (0, 1, or 2)
    num_crabs = random.choice([0, 1, 2])
    for _ in range(num_crabs):
        crab_detection = {
            "class": "Crab",
            "bbox": [
                random.randint(100, 500),  # x
                random.randint(100, 380),  # y
                random.randint(30, 80),  # w
                random.randint(30, 80),  # h
            ],
        }
        detections.append(crab_detection)

    detection_result = {
        "detections": detections,
        "timestamp": time.time(),
    }
    logger.info(f"Detection algorithm completed. Detections: {detections}")
    return detection_result


def detect_qr_code(image):
    """
    Detects QR code in the image and extracts the block ID.
    """
    qr_detector = cv2.QRCodeDetector()
    data, bbox, _ = qr_detector.detectAndDecode(image)
    if data:
        logger.info(f"Detected QR code with data: {data}")
        try:
            block_id = int(data)
            return block_id
        except ValueError:
            logger.error("QR code data is not a valid integer block ID.")
            return None
    else:
        logger.warning("No QR code detected.")
        return None
