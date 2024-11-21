import cv2 as cv

def testDevice(source):
   cap = cv.VideoCapture(source)
   if cap is None or not cap.isOpened():
       print('Warning: unable to open video source: ', source)

testDevice("rtsp://admin:punkengmak7745@192.168.1.100/Streaming/Channels/1") # no printout
