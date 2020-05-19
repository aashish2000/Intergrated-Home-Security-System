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

# Evaluates if motion is present to start the recognition process
def evaluate_picture(camera):
    for filename in glob.glob("motion*"):
        os.remove(filename)

    difference = 20
    pixel_threshold = 100

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

    def capture_face_image(width, height,path_to_img):
        time = datetime.now()
        if os.path.exists(path_to_img):
            os.remove(path_to_img)
        filename = 'motion-%04d%02d%02d-%02d%02d%02d.jpg' % (time.year, time.month,time.day, time.hour,time.minute, time.second)
        camera.resolution = (width, height)
        camera.capture(filename)
        print('Captured %s' % filename)
        return(filename)

    image1, buffer1 = compare()

    timestamp = time.time()
    path_to_img=''
    finalnames=[]

    while (True):
        image2, buffer2 = compare()
        '''
        Motion detection is calculated by calculating the difference in pixel_threshold between
        consecutive frames to identify movemement.
        '''
        changedpixels = 0
        for x in range(0, 100):
            for y in range(0, 75):
                pixdiff = abs(buffer1[x,y][1]- buffer2[x,y][1])
                if pixdiff > difference:        
                    changedpixels += 1
        
        # Check if pixel difference is grater than threshold 
        if changedpixels > pixel_threshold:
            timestamp = time.time()
            path_to_img=capture_face_image(width, height,path_to_img)

            # Run face decection 
            detected_image,detected_face_coords,no_detected_faces=detect(path_to_img)
            if(no_detected_faces>0):
                image1 = image2
                buffer1 = buffer2
                recognize(detected_image,detected_face_coords)
        image1 = image2
        buffer1 = buffer2

