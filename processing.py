import asyncio
from logger import logger
from hardware import shift_camera, shift_raft
from config import SHIFT_INTERVAL, X_STEP, Y_STEP, HARDWARE_DEV_MODE, CREDENTIAL, BACKEND_URL, API_DEV_MODE
import requests

current_x = 0
current_y = 0

raft_id = None

with open("raft_id.txt", "r") as f:
    raft_id = f.read()

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
        if not API_DEV_MODE:
            await send_data_via_api(processed_data)
        else:
            logger.info("API_DEV_MODE enabled. Skipping API call.")
    
        detection_queue.task_done()


async def post_process_data(detection_result):
    """
    Processes detection results to determine molting status.
    """
    await asyncio.sleep(0.2)  # Simulate processing time

    boxes = detection_result["boxes"]
    crabs = detection_result["crabs"]

    molting_status = {}

    for box in boxes:
        box_id = box.get("box_id")
        if box_id is None:
            logger.info("Box without a verified ID. Skipping molting check.")
            continue

        box_bbox = box["bbox"]

        # Find crabs within the bounds of this box
        crabs_in_box = [
            crab for crab in crabs if is_crab_in_box(crab["bbox"], box_bbox)
        ]

        # Determine molting status
        if len(crabs_in_box) == 2:
            status = "Molting"
        else:
            status = "Not Molting"

        molting_status[box_id] = {
            "status": status,
            "crab_count": len(crabs_in_box),
            "crabs": crabs_in_box,
        }

    processed_data = {
        "molting_status": molting_status,
        "timestamp": detection_result["timestamp"],
    }
    logger.info(f"Post-processing completed. Molting status: {molting_status}")
    return processed_data


def is_crab_in_box(crab_bbox, box_bbox):
    """
    Determines if a crab is inside a box based on bounding boxes.
    """
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
    # format body in server side(per box)
    # class BoxUpdateRequestBody(BaseModel):
    # lisense: str
    # raft_id: int
    # box_id: int
    # status: BoxStatus
    # await asyncio.sleep(0.1)
    
    
    for box_id, data in processed_data["molting_status"].items():
        status = data["status"]
        crabs = data["crabs"]
        
        body = {
            "lisense": CREDENTIAL,
            "raft_id": raft_id,
            "box_id": box_id,
            "status": status,
        }
        
        response = requests.post(f"{BACKEND_URL}/backapi/pi/update_box", json=body)
        if response.status_code != 200:
            logger.error(f"Failed to send data for box {box_id}.")
            continue
        logger.info(f"Data sent via API for box {box_id}: {body}")
        
    logger.info(f"Data sent via API: {processed_data}")


async def force_shift_camera():
    """
    Coroutine to force shift the camera every TIME_INTERVAL seconds.
    """
    global current_x, current_y
    # move x when y is done and vice versa
    if current_y < Y_STEP:
        if not HARDWARE_DEV_MODE:
            await shift_raft()
        current_y += 1
        logger.info("Raft has been shifted.")

    if current_y == Y_STEP:
        if current_x < X_STEP:
            await shift_camera()
            current_x += 1
            logger.info("Camera has been shifted.")
        else:
            current_x = 0
            current_y = 0
            logger.info("Camera and raft have been shifted.")

