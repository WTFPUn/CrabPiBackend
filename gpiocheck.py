import gpiod

try:
    chip = gpiod.Chip("gpiochip4")
    print("Successfully accessed gpiochip4!")
except Exception as e:
    print("Failed to access gpiochip4:", e)