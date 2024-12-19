import asyncio
from logger import logger
from hardware import shift_camera, shift_raft, fuckingback
from config import SHIFT_INTERVAL, ROW_BOX, COL_BOX, HARDWARE_DEV_MODE, CREDENTIAL, BACKEND_URL, API_DEV_MODE
import requests
import base64
import io
import numpy as np
from PIL import Image


current_x = 0
current_y = 0

raft_id = None

def numpy_to_base64(image_array, image_format="JPEG"):
    # Convert the NumPy array (H x W x C) to a PIL Image
    # Ensure your array is in the right format: for RGB images, typically uint8 type.
    image_array = image_array[..., ::-1]
    pil_image = Image.fromarray(image_array.astype('uint8'))

    # Write the image to a bytes buffer in the specified format
    buffer = io.BytesIO()
    pil_image.save(buffer, format=image_format)
    buffer.seek(0)

    # Base64 encode the bytes
    img_bytes = buffer.getvalue()
    base64_str = base64.b64encode(img_bytes).decode('utf-8')

    return base64_str


async def post_process_module(detection_queue: asyncio.Queue):
    """
    Coroutine that processes detection results and sends data via API.
    """
    while True:
        logger.info("runn post")

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
            status = "MOLT"
        elif len(crabs_in_box) == 1:
            status = "NOT_MOLT"
        else:
            status = "EMPTY"



        molting_status[box_id] = {
            "status": status,
            "crab_count": len(crabs_in_box),
            "crabs": crabs_in_box,
            "img": numpy_to_base64(box["img"])
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
    with open("raft_id.txt", "r") as f:
        raft_id = f.read()

    for box_id, data in processed_data["molting_status"].items():
        status = data["status"]
        crabs = data["crabs"]

        body = {
            "lisense": CREDENTIAL,
            "raft_id": raft_id,
            "box_id": int(box_id),
            "status": status,
            "image": data["img"]
        }
        logger.info(BACKEND_URL)
        response = requests.post(f"https://harvesttech-scraber.com/backapi/pi/update_box", json=body)
        if response.status_code != 200:
            logger.error(f"Failed to send data for box {box_id}.")
            continue
        logger.info(f"Data sent via API for box {box_id}: {body}")

    logger.info(f"Data sent via API: {processed_data}")


async def force_shift_camera(t):
    """
    Coroutine to force shift the camera every TIME_INTERVAL seconds.
    """
    global current_x, current_y
    # move x when y is done and vice versa
    if current_y < ROW_BOX:
        await shift_raft(t)
        current_y += 1
        logger.info("Raft has been shifted.")

    if current_y == ROW_BOX:
        if current_x < COL_BOX:
            await shift_camera()
            current_x += 1
            current_y = 0
            logger.info("Camera has been shifted.")
        else:
            await fuckingback()
            current_x = 0
            current_y = 0
            exit(1)
            logger.info("fucking stop")

