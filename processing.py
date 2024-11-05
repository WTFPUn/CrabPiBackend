import asyncio
import time
from config import TIME_INTERVAL
from hardware import shift_camera
from logger import logger


async def post_process_module(detection_queue: asyncio.Queue):
    """
    Coroutine that processes detection results and sends data via API.
    """
    while True:
        detection_result = await detection_queue.get()
        logger.info("Post-process module processing detection result.")

        # Process detection results
        processed_data = await post_process_data(detection_result)

        # Simulate sending data via API
        await send_data_via_api(processed_data)

        detection_queue.task_done()


async def post_process_data(detection_result):
    """
    Processes detection results to determine molting status.
    """
    await asyncio.sleep(0.2)  # Simulate processing time

    # Separate detections into 'Crab' and 'Box'
    crabs = [det for det in detection_result["detections"] if det["class"] == "Crab"]
    boxes = [det for det in detection_result["detections"] if det["class"] == "Box"]

    molting_status = {}
    for box in boxes:
        block_id = box.get("block_id")
        if block_id is None:
            logger.warning("Block ID not found. Skipping this box.")
            continue

        box_bbox = box["bbox"]
        crabs_in_box = [
            crab for crab in crabs if is_crab_in_box(crab["bbox"], box_bbox)
        ]

        status = "Molting" if len(crabs_in_box) == 2 else "Not Molting"
        molting_status[block_id] = {"status": status, "crab_count": len(crabs_in_box)}

    processed_data = {
        "molting_status": molting_status,
        "timestamp": detection_result["timestamp"],
    }
    logger.info(f"Post-processing completed. Molting status: {molting_status}")
    return processed_data


def is_crab_in_box(crab_bbox, box_bbox):
    crab_x, crab_y, crab_w, crab_h = crab_bbox
    box_x, box_y, box_w, box_h = box_bbox

    crab_center_x = crab_x + crab_w / 2
    crab_center_y = crab_y + crab_h / 2

    in_x = box_x <= crab_center_x <= box_x + box_w
    in_y = box_y <= crab_center_y <= box_y + box_h

    return in_x and in_y


async def send_data_via_api(processed_data):
    """
    Simulate sending data via an API.
    """
    await asyncio.sleep(0.1)
    logger.info(f"Data sent via API: {processed_data}")


async def force_shift_camera():
    """
    Coroutine to force shift the camera every TIME_INTERVAL seconds.
    """
    while True:
        await asyncio.sleep(TIME_INTERVAL)
        shift_camera()
