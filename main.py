import asyncio
from capture import capture_images
from detection import detection_module
from processing import post_process_module, force_shift_camera
import requests
from config import BACKEND_URL, CREDENTIAL, ROW_BOX, COL_BOX
from logger import logger

# check = requests.post("{}/backapi/pi/init_pond".format(BACKEND_URL), json= {
#     "lisense": CREDENTIAL,
#     "raft_info": [
#         {"row": ROW_BOX, "column": COL_BOX}
#     ]
# })

# print(check.status_code)
# if check.status_code != 200:
#     print("Liscense not valid")
#     exit(1)



# raft_id = check.text
# logger.info(raft_id)


# keep raft_id in file
# with open("raft_id.txt", "w") as f:
#     f.write(raft_id)

async def main():
    image_queue = asyncio.Queue()
    detection_queue = asyncio.Queue()
    print("set queue")

    # Start the coroutines, including the force shift camera coroutine
    tasks = [
        asyncio.create_task(capture_images(image_queue)),
        asyncio.create_task(detection_module(image_queue, detection_queue)),
        asyncio.create_task(post_process_module(detection_queue)),
    ]

    print("set tasks")

    # Run the tasks indefinitely
    await asyncio.gather(*tasks)


# Run the main function
loop = asyncio.get_event_loop()
print("Get loop")
loop.run_until_complete(main())