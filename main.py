import asyncio
from capture import capture_images
from detection import detection_module
from processing import post_process_module, force_shift_camera


async def main():
    image_queue = asyncio.Queue()
    detection_queue = asyncio.Queue()

    # Start the coroutines, including the force shift camera coroutine
    tasks = [
        asyncio.create_task(capture_images(image_queue)),
        asyncio.create_task(detection_module(image_queue, detection_queue)),
        asyncio.create_task(post_process_module(detection_queue)),
    ]

    # Run the tasks indefinitely
    await asyncio.gather(*tasks)


# Run the main function
asyncio.run(main())
