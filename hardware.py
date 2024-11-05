import gpiod
from config import X_AXIS_PIN, Y_AXIS_PIN

chip = gpiod.Chip("gpiochip4")
# set the line to output
# line = chip.get_line(PWM_PIN)
# line.request(consumer="pwm", type=gpiod.LINE_REQ_DIR_OUT)

x_line = chip.get_line(X_AXIS_PIN)
y_line = chip.get_line(Y_AXIS_PIN)


def shift_camera():
    """
    Function to shift x axis(camera)
    """
    x_line.set_value(1)
    x_line.set_value(0)


def shift_raft():
    """
    Function to shift y axis(raft)
    """
    y_line.set_value(1)
    y_line.set_value(0)
