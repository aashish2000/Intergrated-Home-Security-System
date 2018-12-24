# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
import RPi.GPIO as GPIO
from face_recognition.face_recognition_cli import image_files_in_folder
from predict import predict
import time
import datetime
import tkinter as tk
import csv
import os
import ast

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
def recognize(imgdata,faceloc):
    GPIO.setwarnings(False)
    mydict={}

    def LabelDisp(finalnames):
        def clear_label():
            #print ("clear_label")
            label.grid_forget()
            root2.destroy()

        root2 = tk.Toplevel()
        root2.title("  ")
        windowWidth = root2.winfo_reqwidth()
        windowHeight = root2.winfo_reqheight()
        root2.rowconfigure(0, weight=1)        
        root2.grid_columnconfigure(0, weight=1)
         
        # Gets both half the screen width/height and window width/height
        positionRight = int(root2.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root2.winfo_screenheight()/2 - windowHeight/2)
        root2.geometry("+{}+{}".format(positionRight, positionDown))

        if(finalnames[0]!="Unknown"):
            label = tk.Label(root2,text="Welcome "+','.join(finalnames),font=('Calibri',18))
        else:
            label = tk.Label(root2,text="Unknown Faces Detected",font=('Calibri',18))     
        label.grid(row=0, column=0,sticky='nsew', padx=5, pady=5)
        label.after(10000, clear_label)    # 1000ms

        
    namelist=[]
    
    in1 = 16
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.output(in1, False)
    #camera = picamera.PiCamera()
    '''camera.resolution = (320, 240)
    output = np.empty((240, 320, 3), dtype=np.uint8)'''

    # Load a sample picture and learn how to recognize it.
    print("Loading known face image(s)")
    #aash_image = face_recognition.load_image_file("/home/pi/Desktop/FaceRec/Aash1.jpg")
    #aash_face_encoding = face_recognition.face_encodings(aash_image)[0]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    t=0
    print("Capturing image.")
    
    # Grab a single frame of video from the RPi camera as a numpy array
    '''camera.capture(output, format="rgb")'''
    count=0
    f=0

        # Find all the faces and face encodings in the current frame of video
    predictions=predict(imgdata,faceloc, knn_clf=None, model_path="trained_knn_model.clf")
    for name in predictions:
         f=1
         ts = time.time()
         st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
         if(name[0]=="unknown"):
             count+=1
             
         else:
             print("Welcome "+name[0])
             namelist.append(name[0])
         mydict[name[0]]=st
         t+=1
             
    '''t+=1
    if(t==10):
         print("No of tries exceedeed")
         break'''
    if(count==0 and f!=0):
         GPIO.output(in1, True)
    else:
         print("Unknown Faces Detected, Try Again")
         namelist.append("Unknown")
         os.system('cp ./[m]* ./UnknownFaces')

    if(namelist!=[]):
        with open('dict.csv', 'a', newline='') as csv_file:
            writer=csv.writer(csv_file)
            for enc in mydict.items():
                    writer.writerow(enc)
        LabelDisp(namelist)
        time.sleep(10)
        GPIO.output(in1, False)
        
