from tkinter import *
from tkinter import messagebox
import time
import datetime
import os
import sys
import csv
import ast
import RPi.GPIO as GPIO
import glob
import picamera
from FaceDetection import detect


camera=picamera.PiCamera()

def RecFace():
    #os.system('python3 RecognitionGUI.py')
    os.system('python3 RecognitionGUI.py')
def Exit():
    sys.exit(0)
def EncFace():
    os.system('python3 EncodeGUI.py')
def Surveill():
    os.system('python3 Surveillance.py --output output --picamera 1')
def Visitor():
    os.system('libreoffice --calc --view dict.csv')
def Override():
    GPIO.setwarnings(False)
    mydict={}
    camera.resolution=(320,240)
    now = datetime.datetime.now()
    filename = 'motion-%04d%02d%02d-%02d%02d%02d.jpg' % (now.year, now.month,now.day, now.hour,now.minute, now.second)
    camera.capture(filename)
    st = now.strftime('%Y-%m-%d %H:%M:%S')
    im,loc,num=detect(filename)
    if(num>0):
        val=messagebox.askquestion(" ","Face Detected, Unlock now?")
        if(val=='yes'):
            mydict["Manual Override"]=st
            os.system("mv ./[m]* ./OverrideFaces")
            in1 = 16
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(in1, GPIO.OUT)
            GPIO.output(in1, True)
            time.sleep(10)
            GPIO.output(in1, False)
            messagebox.showinfo(" ","Entry Authorized")
        else:
            mydict["Unauthorized"]=st            
            messagebox.showinfo(" ","Entry Unauthorized")
            os.system("mv ./[o]* ./OverrideFaces")
        with open('/home/pi/Desktop/Intergrated-Home-Security-System/dict.csv', 'a', newline='') as csv_file:
            writer=csv.writer(csv_file)
            for enc in mydict.items():
                    writer.writerow(enc)
    else:
        messagebox.showinfo(" ","No faces Detected")

    for filename in glob.glob("motion*"):
        os.remove(filename)
        

root = Tk()
frame=Frame(root)
width, height = frame.winfo_screenwidth(), frame.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width,height))
root.attributes("-fullscreen",True)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N+S+E+W)
grid=Frame(frame)
grid.grid(sticky=N+S+E+W, column=0, row=7)
Grid.rowconfigure(frame, 7, weight=1)
Grid.columnconfigure(frame, 0, weight=1)

Label(frame, text="Intergrated Face Recognition System: ",font=('Calibri',20),borderwidth=1, relief="solid").grid(row=0,column=0,columnspan=10,
               rowspan=2,sticky=W+E+N+S, padx=5, pady=5)
#example values
'''for x in range(10):
    for y in range(5):
        btn = Button(frame)
        btn.grid(column=x, row=y, sticky=N+S+E+W)'''
btn1 = Button(frame,text="Encode Face",font=('Calibri',17),command=EncFace)
btn1.grid(column=2, row=3, sticky=N+S+E+W)
btn2 = Button(frame,text="Recognition",font=('Calibri',17),command=RecFace)
btn2.grid(column=5, row=2, sticky=N+S+E+W)
btn3 = Button(frame,text="Surveillance",font=('Calibri',17),command=Surveill)
btn3.grid(column=8, row=3, sticky=N+S+E+W)
btn4 = Button(frame,text="Visitor Log",font=('Calibri',17),command=Visitor)
btn4.grid(column=5, row=4, sticky=N+S+E+W)
btn5 = Button(frame,text="Exit",font=('Calibri',17),command=Exit)
btn5.grid(column=9, row=5, sticky=N+S+E+W)
btn6 = Button(frame,text="Manual Override",font=('Calibri',17),command=Override)
btn6.grid(column=0, row=5, sticky=N+S+E+W)



for x in range(10):
    Grid.columnconfigure(frame, x, weight=1)

for y in range(5):
    Grid.rowconfigure(frame, y, weight=1)

root.mainloop()
