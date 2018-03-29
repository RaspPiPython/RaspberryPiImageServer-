# Test send 1 image
import socket
import pickle
import time
import sys
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

HOST = '192.168.0.103'
PORT = 50009
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

#conn.close()



# Capture the image
timestart = time.time()
camera = PiCamera()
rawCapture = PiRGBArray(camera)
#elapsedtime3=time.time()-timestart
time.sleep(0.1)  #remember to substract warmup time
#elapsedtime5=time.time()-timestart
#camera.resolution=(320,240)  #set resolution takes around 0.17s
                              #default resolution is 640x480
#elapsedtime6=time.time()-timestart
camera.capture(rawCapture, format='bgr') #capture individual image takes 
                #0.48s because camera need adjustment for individual images
#elapsedtime4=time.time()-timestart
image = rawCapture.array
#elapsedtime1=time.time()-timestart
imageData = pickle.dumps(image) #pickle takes ~10ms for 640x480 frame
imageDataSize = sys.getsizeof(imageData)
imageDataLen = len(imageData)
sizeData = pickle.dumps(imageDataSize)
lenData = pickle.dumps(imageDataLen)
print('Sending size of image data')
conn.send(sizeData)
conn.send(lenData)
print('Sending image data')
conn.send(imageData)



# Make gray scale with 3 channels, stack horizontally to raw image
#grey=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#grey3channel=cv2.cvtColor( grey, cv2.COLOR_GRAY2RGB)
#imageHorizontal=np.hstack((image, grey3channel))
#cv2.imshow('Stacked image', imageHorizontal)


conn.close()


elapsedtime2=time.time()-timestart



#cv2.waitKey(0)

#print(image.shape)
#print(imageHorizontal.shape)

#print(elapsedtime3)
#print(elapsedtime5)
#print(elapsedtime6)
#print(elapsedtime4)
#print(elapsedtime1)
print('Total elapsed time:', elapsedtime2)
s.close()
s = None

