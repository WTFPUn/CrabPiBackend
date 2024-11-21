import cv2
import os
import random



choice = os.listdir("imgs")
candidate = random.choice(choice)
print("candidate is: ", candidate)
image = cv2.imread(f"imgs/{random.choice(choice)}")
print("size", image.shape)
shape = image.shape
image = cv2.resize(image, (shape[1], shape[0]))
# imagr = cv2.resize(cv2.imread('Download/full.jpg', 0), (0, 0), fx=0.2, fy=0.17)
qr_detector = cv2.QRCodeDetector()
data, _, _ = qr_detector.detectAndDecode(image)
print(data)
if data:
    try:
        box_id = int(data)
        print(f"QR code detected in box with ID: {box_id}")
    except ValueError:
        print("QR code data is not a valid integer.")
else:
    print("No QR code detected in box.")