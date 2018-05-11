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
    
    # allow the camera to warmup
    time.sleep(1)

    # initialize GPIO pins
    #Control = CarControlFunc.PiCarCtrl()

    # capture frames from the camera
    print('<INFO> Preparing to stream video...')
    timeStart = time.time()
    for frame in camera.capture_continuous(rawCapture, format="bgr",
                                           use_video_port = True):
        command = ImageServer.recvCommand()
        #if command == 'BYE':
            #ImageServer.sendCommand('ACK')
        #    print('BYE received, ending stream session...')
        #    break

        # grab the raw NumPy array representing the image, then initialize 
        # the timestamp and occupied/unoccupied text
        image = frame.array
        ret, compressedImg = cv2.imencode('.jpg', image)
        imageData = pickle.dumps(compressedImg) 
        ImageServer.sendFrame(imageData) # send the frame data

        # clear the stream in preparation for the next one
        rawCapture.truncate(0)

        if time.time() - timeStart >= 20:
            break
        
    print('<INFO> Video stream ended')
    ImageServer.closeServer()

    elapsedTime = time.time() - timeStart
    print('<INFO> Total elapsed time is: ', elapsedTime)


    
def main3():
    client_socket = socket.socket()
    client_socket.connect(('my_server', 8000))
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 30
            time.sleep(2)
            start = time.time()
            stream = io.BytesIO()
            # Use the video-port for captures...
            for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                if time.time() - start > 30:
                    break
                stream.seek(0)
                stream.truncate()
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()
    

def main2():
    # initialize the server and time stamp
    ImageServer = PiImageServer()
    ImageServer.openServer('192.168.1.89', 50009)
    
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

    # initialize GPIO pins
    Control = CarControlFunc.PiCarCtrl()

    # capture frames from the camera
    print('<INFO> Preparing to stream video...')
    timeStart = time.time()
    for frame in camera.capture_continuous(rawCapture, format="bgr",
                                           use_video_port = True):
        command = ImageServer2.recvCommand()
        if command == 'BYE':
            #ImageServer.sendCommand('ACK')
            print('BYE received, ending stream session...')
            break

        # grab the raw NumPy array representing the image, then initialize 
        # the timestamp and occupied/unoccupied text
        image = frame.array               
        #cv2.imshow('Frame', image)
        #key = cv2.waitKey(1) & 0xFF # catch any key input
        imageData = pickle.dumps(image) 
        ImageServer.sendFrame(imageData) # send the frame data

        # clear the stream in preparation for the next one
        rawCapture.truncate(0)
        
    print('<INFO> Video stream ended')
    ImageServer.closeServer()
    ImageServer2.closeServer()

    elapsedTime = time.time() - timeStart
    print('<INFO> Total elapsed time is: ', elapsedTime)
    

if __name__ == '__main__': main()



    


    
