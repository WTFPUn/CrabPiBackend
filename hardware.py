import serial
import time
import asyncio
from config import X_AXIS_PIN, Y_AXIS_PIN
from logger import logger
from config import HARDWARE_DEV_MODE, RAFT_SHIFT_TIME, CAM_SHIFT_TIME

if not HARDWARE_DEV_MODE:
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout= 1)
    time.sleep(2)

def send_data(data):
    ser.write(data.encode())
    logger.info("send data to move")

async def shift_camera():
    """
    Function to shift x axis(camera)
    """
    if HARDWARE_DEV_MODE:
        logger.info("some cam push")
        await asyncio.sleep(7)
        logger.info("raft stop")
        await asyncio.sleep(5)
    else:
        send_data("forward,88\n")
        await asyncio.sleep(CAM_SHIFT_TIME)
        send_data("stop,0\n")
        logger.info("shift camera")

async def fuckingback():
    send_data("reverse,98\n")
    await asyncio.sleep(7)
    send_data("stop,0\n")

async def shift_raft(t):
    """
    Function to shift y axis(raft)
    """
    logger.info("some raft push")
    await asyncio.sleep(t)
    logger.info("raft stop")
