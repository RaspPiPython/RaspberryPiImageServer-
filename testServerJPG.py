# Test detect whitelanes
import socket
import pickle
import time
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from SendFrameInOO import PiImageServer
import CarControlFunc 

def main():
    # initialize the server and time stamp
    ImageServer = PiImageServer()
    ImageServer2 = PiImageServer()
    #ImageServer.openServer('169.254.233.189', 50009)
    #ImageServer2.openServer('169.254.233.189', 50002)

    #ImageServer.openServer('192.168.1.89', 50009)
    #ImageServer2.openServer('192.168.1.89', 50002)

    # Initialize the camera object
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 10 #it seems this cannot go higher than 10
                          #unless special measures are taken, which may
                          #reduce image quality
    camera.exposure_mode = 'sports' #reduce blur
    rawCapture = PiRGBArray(camera)
    
    # allow the camera to warmup
    time.sleep(1)
    
    #camera.capture(rawCapture, format='bgr')
    #image = rawCapture.array
    #imageData = pickle.dumps(image)

    # initialize GPIO pins
    Control = CarControlFunc.PiCarCtrl()

    # capture frames from the camera
    print('<INFO> Preparing to stream video...')
    timeStart = time.time()
    for frame in camera.capture_continuous(rawCapture, format="bgr",
                                           use_video_port = True):
        # grab the raw NumPy array representing the image, then initialize 
        # the timestamp and occupied/unoccupied text
        print(len(frame), type(frame))
        break
        '''image = frame.array               
        cv2.imshow('Frame', image)
        key = cv2.waitKey(1) & 0xFF # catch any key input
        imageData = pickle.dumps(image) 
        ImageServer.sendFrame(imageData) # send the frame data'''

        # receive command from laptop and print it
        command = ImageServer2.recvCommand()        
        '''if command == 'STR':
            #Control.forward()
            pass
        elif command == 'LFT':
            #Control.left()
            pass
        elif command == 'RGT':
            #Control.right()
            pass
        elif command == 'STP':
            #Control.brake()
            pass
        elif command == 'BYE':
            print('BYE received, ending stream session...')
            break'''
        print(command)
        if command == 'BYE':
            print('BYE received, ending stream session...')
            break        

        # clear the stream in preparation for the next one
        rawCapture.truncate(0)       

        # if the 'q' key is pressed, break from the loop
        if key == ord("q"):           
            break
    print('<INFO> Video stream ended')
    ImageServer.closeServer()

    elapsedTime = time.time() - timeStart
    print('<INFO> Total elapsed time is: ', elapsedTime)

    


if __name__ == '__main__': main()



    


    
