import asyncio
import time
import cv2
import numpy as np
from logger import logger
import random
from config import DETECTION_DEV_MODE, MODEL_PATH
from ultralytics import YOLOWorld

if not DETECTION_DEV_MODE:
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

    if not DETECTION_DEV_MODE:
        # Perform inference using the YOLO-World model
        results = model.predict(image, conf=0.5)
    else:
        results = simulate_detections(image)  # Replace with actual model inference
        await asyncio.sleep(10)  # Simulate processing time

    boxes = []
    crabs = []

    # Iterate over each result
    for result in results:
        # Access the detected boxes
        for box in result.boxes:
            class_id = int(box.cls)
            confidence = float(box.conf)
            x_min, y_min, x_max, y_max = box.xyxy[0].tolist()

            # Convert the coordinates to integers
            x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])

            # Map class IDs to class names
            class_name = model.names[class_id]

            detection = {
                "class": class_name,
                "confidence": confidence,
                "bbox": [x_min, y_min, x_max, y_max]
            }

            logger.info(f"Detection: {class_name} with confidence {confidence}")

            if class_name == "Box":
                # Try to read QR code within the box bounds for box ID
                box_id = detect_qr_code_in_box(image, detection["bbox"])
                if box_id is None:
                    # Skip this box if QR code was not found
                    continue
                detection["box_id"] = box_id  # Add box ID to detection if QR code was found
                boxes.append(detection)
            elif class_name == "Crab":
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
