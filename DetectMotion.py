import io
import glob
import sys
import os
import picamera
import time
from datetime import datetime
import PIL.Image
from FaceDetection import detect
from FaceRecognition import recognize
import tkinter as tk
#from tkinter import messagebox
def motiondet(camera):
    for filename in glob.glob("motion*"):
        os.remove(filename)

    #camera = picamera.PiCamera()

    difference = 20
    pixels = 100

    width = 320
    height = 240

    def compare():
        camera.resolution = (100, 75)
        stream = io.BytesIO()
        camera.capture(stream, format = 'bmp')
        
        stream.seek(0)
        im = PIL.Image.open(stream)
        buffer = im.load()
        stream.close()
        return im, buffer
    def newimage(width, height,oldfile):
        time = datetime.now()
        if os.path.exists(oldfile):
            os.remove(oldfile)
        filename = 'motion-%04d%02d%02d-%02d%02d%02d.jpg' % (time.year, time.month,time.day, time.hour,time.minute, time.second)
        camera.resolution = (width, height)
        camera.capture(filename)
        print('Captured %s' % filename)
        return(filename)

    image1, buffer1 = compare()

    timestamp = time.time()
    oldfile=''
    finalnames=[]

    while (True):
        image2, buffer2 = compare()

        changedpixels = 0
        for x in range(0, 100):
            for y in range(0, 75):
                pixdiff = abs(buffer1[x,y][1]- buffer2[x,y][1])
                if pixdiff > difference:        
                    changedpixels += 1
        if changedpixels > pixels:
            timestamp = time.time()
            oldfile=newimage(width, height,oldfile)
            imgdata,faceloc,n=detect(oldfile)
            if(n>0):
                image1 = image2
                buffer1 = buffer2
                recognize(imgdata,faceloc)
        image1 = image2
        buffer1 = buffer2

