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
def recognize(imgdata,faceloc):
    GPIO.setwarnings(False)
    mydict={}

    def display_message(finalnames):
        def clear_label():
            label.grid_forget()
            root2.destroy()

        root2 = tk.Toplevel()
        root2.title("  ")
        windowWidth = root2.winfo_reqwidth()
        windowHeight = root2.winfo_reqheight()
        root2.rowconfigure(0, weight=1)        
        root2.grid_columnconfigure(0, weight=1)
         
        # Gets both half the screen width/2 and height/2
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

    # Initialize some variables
    face_locations = []
    face_encodings = []
    t=0
    #print("Capturing image.")
    
    count=0
    face_recognized=0

    # Find all the faces and face encodings in the picture
    predictions=predict(imgdata,faceloc, knn_clf=None, model_path="trained_knn_model.clf")
    for name in predictions:
         face_recognized=1
         ts = time.time()
         st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
         if(name[0]=="unknown"):
             count+=1
         else:
             print("Welcome "+name[0])
             namelist.append(name[0]) # Add name to list of recognized people
         mydict[name[0]]=st
         t+=1
    
    # If Faces recognized, open the door
    if(count==0 and face_recognized!=0):
         GPIO.output(in1, True)
    else:
         print("Unknown Faces Detected, Try Again")
         namelist.append("Unknown")
         os.system('cp ./[m]* ./UnknownFaces')

    # Log the entry of recognized induvidual
    if(namelist!=[]):
        with open('dict.csv', 'a', newline='') as csv_file:
            writer=csv.writer(csv_file)
            for enc in mydict.items():
                    writer.writerow(enc)
        display_message(namelist)
        time.sleep(10)
        GPIO.output(in1, False)
        
