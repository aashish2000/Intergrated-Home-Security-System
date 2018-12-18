import tkinter as Tkinter
import os
import glob
import time
import _thread
import random
import picamera
import sys
import RPi.GPIO as GPIO
from DetectMotion import motiondet
def kill():
    GPIO.output(16, False)
    for filename in glob.glob("motion*"):
        os.remove(filename)
    sys.exit(0)

def threadmain():
    camera = picamera.PiCamera()
    motiondet(camera)
if __name__ == '__main__':
    _thread.start_new_thread(threadmain, ())
    root = Tkinter.Tk()
    frame=Tkinter.Frame(root)
    root.attributes("-fullscreen",True)
    Tkinter.Grid.rowconfigure(root, 0, weight=1)
    Tkinter.Grid.columnconfigure(root, 0, weight=1)
    frame.grid(row=0, column=0, sticky='nsew')
    grid=Tkinter.Frame(frame)
    grid.grid(sticky='nsew', column=0, row=7)
    Tkinter.Grid.rowconfigure(frame, 7, weight=1)
    Tkinter.Grid.columnconfigure(frame, 0, weight=1)
    console = Tkinter.Button(frame,text="Back",font=('Comic Sans MS',15),command=kill)
    console.grid(row=4,column=5,sticky='nsew')
    Tkinter.Label(frame, text="Stand in front of the camera",font=('Comic Sans MS',20),borderwidth=1, relief="solid").grid(row=2,column=2,columnspan=6,
                   rowspan=1,sticky='nsew', padx=5, pady=5)

    for x in range(10):
        Tkinter.Grid.columnconfigure(frame, x, weight=1)

    for y in range(5):
        Tkinter.Grid.rowconfigure(frame, y, weight=1)

    Tkinter.Label(frame, text="Recognition Mode",font=('Comic Sans MS',20),borderwidth=1, relief="solid").grid(row=0,column=0,columnspan=10,
                   rowspan=1,sticky='nsew', padx=5, pady=5)
    root.mainloop()
