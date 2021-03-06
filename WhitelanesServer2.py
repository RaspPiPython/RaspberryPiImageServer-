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
    ImageServer.openServer('192.168.1.89', 50009)

    # Initialize the camera object
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 30 #it seems this cannot go higher than 10
                          #unless special measures are taken, which may
                          #reduce image quality
    camera.exposure_mode = 'sports' #reduce blur
    rawCapture = PiRGBArray(camera)
    jpgQuality = 90
    #pngCompression = 3
    
    # allow the camera to warmup
    time.sleep(1)

    # initialize GPIO pins
    Control = CarControlFunc.PiCarCtrl()

    # capture frames from the camera
    print('<INFO> Preparing to stream video...')
    timeStart = time.time()
    for frame in camera.capture_continuous(rawCapture, format="bgr",
                                           use_video_port = True):
        # receive command from laptop and print it
        command = ImageServer.recvCommand()
        if command == 'STR':
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
            break
        elif command == 'SRT':
            print('SRT received, start streaming...')
        else:       
            print('<WARNING> {} received, but it is not a valid command'.format(command))
        
        # grab the raw NumPy array representing the image, then initialize 
        # the timestamp and occupied/unoccupied text
        image = frame.array               
        #cv2.imshow('Frame', image)
        #key = cv2.waitKey(1) & 0xFF # catch any key input
        #print(image[0])
        ret, compressedImg = cv2.imencode('.jpg', image,
                        [int(cv2.IMWRITE_JPEG_QUALITY), jpgQuality])
        #ret, compressedImg = cv2.imencode('.png', image,
        #                [int(cv2.IMWRITE_PNG_COMPRESSION), pngCompression])
        imageData = pickle.dumps(compressedImg) 
        ImageServer.sendFrame(imageData) # send the frame data            

        # clear the stream in preparation for the next one
        rawCapture.truncate(0)       

        # if the 'q' key is pressed, break from the loop
        #if key == ord("q"):           
        #    break
    print('<INFO> Video stream ended')
    ImageServer.closeServer()

    elapsedTime = time.time() - timeStart
    print('<INFO> Total elapsed time is: ', elapsedTime)

    


if __name__ == '__main__': main()



    


    
