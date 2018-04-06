# Test server, written with Object Oriented method
import socket
import pickle
import time
#import sys
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

class PiImageServer:
    def __init__(self):
        self.s = None
        self.conn = None
        self.addr = None
        #self.currentTime = time.time()
        self.currentTime = time.asctime(time.localtime(time.time()))
        self.counter = 0

    def openServer(self, serverIP, serverPort):
        print('<INFO> Opening image server at {}:{}'.format(serverIP,
                                                            serverPort))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((serverIP, serverPort))
        self.s.listen(1)
        print('Waiting for client...')
        self.conn, self.addr = self.s.accept()
        print('Connected by', self.addr)

    def closeServer(self):
        print('<INFO> Closing server...')
        self.conn.close()
        self.s.close()
        #self.currentTime = time.time()
        self.currentTime = time.asctime(time.localtime(time.time()))
        print('Server closed at', self.currentTime)

    def sendOneImage(self, imageData):
        print('<INFO> Sending only one image...')
        imageDataLen = len(imageData)
        lenData = pickle.dumps(imageDataLen)
        print('Sending image length')
        self.conn.send(lenData)
        print('Sending image data')
        self.conn.send(imageData)

    def sendFrame(self, frameData):
        self.counter += 1
        print('Sending frame ', self.counter)
        frameDataLen = len(frameData)
        lenData = pickle.dumps(frameDataLen)        
        self.conn.send(lenData)        
        self.conn.send(frameData)


def main():
    # Initialize server
    ImageServer = PiImageServer()
    ImageServer.openServer('192.168.0.103', 50009)

    # Initialize pi camera
    timeStart = time.time()
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    camera.capture(rawCapture, format='bgr')
    image = rawCapture.array
    imageData = pickle.dumps(image)

    ImageServer.sendOneImage(imageData)
    ImageServer.closeServer()

    elapsedTime = time.time() - timeStart
    print('<INFO> Total elapsed time is: ', elapsedTime)


if __name__ == '__main__': main()
