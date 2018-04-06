import socket
import pickle
import time
import sys
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

HOST = '192.168.0.101' #server IP address
PORT = 50009

# Datagram (udp) socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print ('Socket created')
except:
    sys.exit()

 
# Bind socket 
try :
    s.bind((HOST, PORT))
except:
    sys.exit()

     
print ('Socket bind complete')

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)

time.sleep(0.1)
print('Waiting for client...')
clientIP, addr = s.recvfrom(1024)
clientIP = pickle.loads(clientIP)
print('Message received')
print('The client IP address is', clientIP)
print(addr)

camera.capture(rawCapture, format = 'bgr')
image = rawCapture.array
imageData = pickle.dumps(image)

#s.sendto


#cv2.imshow('Test image', image)
#cv2.waitKey(0)
