import asyncio
import time
import cv2
import numpy as np
from logger import logger
import random
from config import DEV_MODE, MODEL_PATH
from ultralytics import YOLOWorld

if not DEV_MODE:
    model = YOLOWorld(MODEL_PATH)


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
    Run detection algorithm, separate boxes and crabs, and try to read QR codes for box IDs.
    """

    if not DEV_MODE:
        detections = model.predict(image)
    else:    
        detections = simulate_detections(image)  # Replace with actual model inference
        await asyncio.sleep(0.5)  # Simulate processing time
        
    boxes = []
    crabs = []

    for detection in detections:
        if detection["class"] == "Box":
            # Try to read QR code within the box bounds for box ID
            # box_id = detect_qr_code_in_box(image, detection["bbox"])
            # mock
            box_id = random.randint(1, 10)
            detection["box_id"] = box_id  # Add box ID to detection if QR code was found
            boxes.append(detection)
        elif detection["class"] == "Crab":
            crabs.append(detection)

    detection_result = {
        "boxes": boxes,
        "crabs": crabs,
        "timestamp": time.time(),
    }
    logger.info(
        f"Detection algorithm completed. Boxes: {len(boxes)}, Crabs: {len(crabs)}"
    )
    return detection_result


def simulate_detections(image):
    """
    Simulate detections for boxes and crabs.
    """
    return [
        {"class": "Box", "bbox": [100, 100, 200, 200]},  # Simulated box coordinates
        {
            "class": "Crab",
            "bbox": [120, 130, 30, 40],
        },  # Simulated crab within box bounds
        {
            "class": "Crab",
            "bbox": [150, 160, 35, 45],
        },  # Simulated crab within box bounds
        # Add more simulated detections as needed
    ]


def detect_qr_code_in_box(image, bbox):
    """
    Detect and decode a QR code within the bounding box area of the image.
    """
    x, y, w, h = bbox
    box_region = image[y : y + h, x : x + w]  # Crop the box region

    qr_detector = cv2.QRCodeDetector()
    data, _, _ = qr_detector.detectAndDecode(box_region)
    if data:
        try:
            box_id = int(data)
            logger.info(f"QR code detected in box with ID: {box_id}")
            return box_id
        except ValueError:
            logger.warning("QR code data is not a valid integer.")
    else:
        logger.info("No QR code detected in box.")
    return None
