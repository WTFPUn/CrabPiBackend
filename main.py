import asyncio
import random
import time

# Simulate hardware interaction libraries
# For Raspberry Pi, you might use picamera and RPi.GPIO
# import picamera
# import RPi.GPIO as GPIO

# For demonstration purposes, we'll simulate image capture and hardware control


class CameraController:
    """
    Controls the camera position and keeps track of the current box IDs.
    """

    def __init__(self, total_boxes=100):
        self.total_boxes = total_boxes
        self.current_box_id = 0  # Start from box 0

    def shift_camera(self):
        """
        Shifts the camera to the next set of boxes.
        """
        if self.current_box_id >= self.total_boxes:
            self.current_box_id = 0  # Reset to the beginning if we've reached the end
            print("Completed scanning all boxes. Resetting to box 0.")

        # Simulate shifting the camera to see the next 4 boxes
        print(
            f"Shifting camera to view boxes: {self.current_box_id}, {self.current_box_id + 1}, "
            f"{self.current_box_id + 2}, {self.current_box_id + 3}"
        )

        # Implement hardware control to physically move the camera here
        # For example, using GPIO pins to control motors

        # Update the current box ID for the next shift
        self.current_box_id += 4


async def capture_images(image_queue, camera_controller):
    """
    Coroutine that captures images and puts them into the queue.
    """
    while True:
        # Simulate image capture
        image = f"image_data_at_box_{camera_controller.current_box_id - 4}"
        print(
            f"Captured image at boxes {camera_controller.current_box_id - 4} to {camera_controller.current_box_id - 1} and put into queue."
        )
        await image_queue.put(image)

        await asyncio.sleep(1)  # Adjust the delay as needed


async def detection_module(image_queue, detection_queue):
    """
    Coroutine that processes images from the image_queue,
    runs detection, and puts results into detection_queue.
    """
    while True:
        image = await image_queue.get()
        print("Detection module processing image.")

        # Simulate detection processing
        detection_result = await run_detection_algorithm(image)

        # Put the detection result into the next queue for post-processing
        await detection_queue.put(detection_result)
        image_queue.task_done()


async def run_detection_algorithm(image):
    """
    Simulate a detection algorithm processing.
    """
    await asyncio.sleep(0.5)  # Simulate processing time

    # Simulate detection results with 'Crab' and 'Box' classes
    classes = ["Crab", "Box"]
    detections = []

    # Simulate detections for 4 boxes
    for box_offset in range(4):
        box_id = int(image.split("_")[-1]) + box_offset
        # Each box detection
        box_detection = {
            "class": "Box",
            "box_id": box_id,
            "bbox": [
                random.randint(0, 100),
                random.randint(0, 100),
                random.randint(50, 150),
                random.randint(50, 150),
            ],  # x, y, w, h
        }
        detections.append(box_detection)

        # Randomly decide how many crabs are in this box (0, 1, or 2)
        num_crabs = random.choice([0, 1, 2])
        for _ in range(num_crabs):
            crab_detection = {
                "class": "Crab",
                "bbox": [
                    random.randint(0, 100),
                    random.randint(0, 100),
                    random.randint(30, 80),
                    random.randint(30, 80),
                ],  # x, y, w, h
            }
            detections.append(crab_detection)

    detection_result = {
        "detections": detections,
        "timestamp": time.time(),
    }
    print(f"Detection algorithm completed. Detections: {detections}")
    return detection_result


async def post_process_module(detection_queue, camera_controller):
    """
    Coroutine that processes detection results and sends data via API.
    """
    while True:
        detection_result = await detection_queue.get()
        print("Post-process module processing detection result.")

        # Process detection results
        processed_data = await post_process_data(detection_result)

        # Simulate sending data via API
        await send_data_via_api(processed_data)

        # Shift the camera to the next position
        camera_controller.shift_camera()

        detection_queue.task_done()


async def post_process_data(detection_result):
    """
    Processes detection results to determine molting status.
    """
    await asyncio.sleep(0.2)  # Simulate processing time

    # Separate detections into 'Crab' and 'Box'
    crabs = [det for det in detection_result["detections"] if det["class"] == "Crab"]
    boxes = [det for det in detection_result["detections"] if det["class"] == "Box"]

    # For each box, find crabs inside it
    molting_status = {}
    for box in boxes:
        box_id = box["box_id"]
        box_bbox = box["bbox"]

        # Find crabs inside this box
        crabs_in_box = []
        for crab in crabs:
            if is_crab_in_box(crab["bbox"], box_bbox):
                crabs_in_box.append(crab)

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
    print(f"Post-processing completed. Molting status: {molting_status}")
    return processed_data


def is_crab_in_box(crab_bbox, box_bbox):
    """
    Determines if a crab is inside a box based on bounding boxes.
    """
    # Simple overlap check between crab and box bounding boxes
    crab_x, crab_y, crab_w, crab_h = crab_bbox
    box_x, box_y, box_w, box_h = box_bbox

    # Check if crab bbox is within box bbox
    in_x = box_x <= crab_x <= box_x + box_w
    in_y = box_y <= crab_y <= box_y + box_h
    return in_x and in_y


async def send_data_via_api(processed_data):
    """
    Simulate sending data via an API.
    """
    await asyncio.sleep(0.1)  # Simulate network delay
    # Use an HTTP client like aiohttp to send data to an API endpoint
    # For demonstration, we'll just print the data
    print(f"Data sent via API: {processed_data}")


async def main():
    image_queue = asyncio.Queue()
    detection_queue = asyncio.Queue()

    # Initialize the camera controller
    camera_controller = CameraController(total_boxes=100)
    camera_controller.shift_camera()  # Initial shift to start at box 0

    # Start the coroutines
    tasks = [
        asyncio.create_task(capture_images(image_queue, camera_controller)),
        asyncio.create_task(detection_module(image_queue, detection_queue)),
        asyncio.create_task(post_process_module(detection_queue, camera_controller)),
    ]

    # Run the tasks indefinitely
    await asyncio.gather(*tasks)


# Run the main function
asyncio.run(main())
