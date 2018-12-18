from tkinter import *
import os

def RecFace():
    #os.system('python3 RecognitionGUI.py')
    os.system('python3 RecognitionGUI.py')
        
def EncFace():
    os.system('python3 EncodeGUI.py')
def Surveill():
    os.system('python3 Surveillance.py --output output --picamera 1')

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

Label(frame, text="Intergrated Face Recognition System: ",font=('Comic Sans MS',20),borderwidth=1, relief="solid").grid(row=0,column=0,columnspan=10,
               rowspan=2,sticky=W+E+N+S, padx=5, pady=5)
#example values
'''for x in range(10):
    for y in range(5):
        btn = Button(frame)
        btn.grid(column=x, row=y, sticky=N+S+E+W)'''
btn1 = Button(frame,text="Encode Face",font=('Comic Sans MS',15),command=EncFace)
btn1.grid(column=2, row=4, sticky=N+S+E+W)
btn2 = Button(frame,text="Recognition",font=('Comic Sans MS',15),command=RecFace)
btn2.grid(column=5, row=4, sticky=N+S+E+W)
btn3 = Button(frame,text="Surveillance",font=('Comic Sans MS',15),command=Surveill)
btn3.grid(column=8, row=4, sticky=N+S+E+W)



for x in range(10):
    Grid.columnconfigure(frame, x, weight=1)

for y in range(5):
    Grid.rowconfigure(frame, y, weight=1)

root.mainloop()
