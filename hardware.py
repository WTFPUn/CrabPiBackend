import gpiod
from gpiod.line import Direction, Value
from config import X_AXIS_PIN, Y_AXIS_PIN


def shift_camera():
    """
    Function to shift x axis(camera)
    """
    with gpiod.request_lines("/dev/gpiochip4", consumer="movecam", config={
        X_AXIS_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE)
    }) as request:

        request.set_value(X_AXIS_PIN, 1)
        #request.set_value(X_AXIS_PIN, 0)


def shift_raft():
    """
    Function to shift y axis(raft)
    """
    with gpiod.request_lines("/dev/gpiochip4", consumer="movecam", config={
        Y_AXIS_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE)
    }) as request:

        request.set_value(Y_AXIS_PIN, 1)
        #request.set_value(Y_AXIS_PIN, 0)

