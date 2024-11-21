import RPi.GPIO as GPIO
from time import sleep
from gpiozero import PWMOutputDevice

# กำหนดหมายเลขพิน
RPWM_PIN = 18  # GPIO 18 สำหรับหมุนไปข้างหน้า
LPWM_PIN = 19  # GPIO 19 สำหรับหมุนไปข้างหลัง

# ตั้งค่า GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RPWM_PIN, GPIO.OUT)
GPIO.setup(LPWM_PIN, GPIO.OUT)

# กำหนด PWM Output บนพินที่ควบคุม
rpwm = PWMOutputDevice(RPWM_PIN)
lpwm = PWMOutputDevice(LPWM_PIN)

# ฟังก์ชันเพื่อหมุนไปข้างหน้า
def rotate_forward(speed=0.5, duration=5):
    rpwm.value = speed  # ความเร็วเป็นเปอร์เซ็นต์ 0.0 ถึง 1.0
    lpwm.value = 0
    print("Motor moving forward with speed:", speed)
    sleep(duration)
    stop_motor()

# ฟังก์ชันเพื่อหมุนไปข้างหลัง
def rotate_backward(speed=0.5, duration=5):
    lpwm.value = speed
    rpwm.value = 0
    print("Motor moving backward with speed:", speed)
    sleep(duration)
    stop_motor()

# ฟังก์ชันหยุดมอเตอร์
def stop_motor():
    rpwm.value = 0
    lpwm.value = 0
    print("Motor stopped")

# ตัวอย่างการใช้งาน
try:
    while True:
        rotate_forward(speed=0.3, duration=5)  # หมุนไปข้างหน้าที่ความเร็ว 50% นาน 5 วินาที
        sleep(1)
        rotate_backward(speed=0.3, duration=5)  # หมุนไปข้างหลังที่ความเร็ว 50% นาน 5 วินาที
        sleep(1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    stop_motor()
    GPIO.cleanup()
