import serial
import time
import asyncio
from config import X_AXIS_PIN, Y_AXIS_PIN
from logger import logger
from config import HARDWARE_DEV_MODE

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
        await asyncio.sleep(5)
        logger.info("raft stop")
        await asyncio.sleep(5)
    else: 
        send_data("forward,128\n")
        await asyncio.sleep(5)
        send_data("stop,0\n")
        await asyncio.sleep(5)
        logger.info("shift camera")

async def shift_raft():
    """
    Function to shift y axis(raft)
    """
    logger.info("some raft push")
    await asyncio.sleep(5)
    logger.info("raft stop")
    await asyncio.sleep(5)
