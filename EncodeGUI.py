from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import os,os.path
import sys
import dlib
#import matplotlib.pyplot as plt
from PIL import Image
import threading

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

def progress():
    def task(root2):
        ft = Frame(root2)
        ft.pack(expand=True, fill=BOTH, side=TOP)
        pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
        pb_hD.pack(expand=True, fill=BOTH, side=TOP)
        pb_hD.start(50)
        root2.mainloop()

    # Define the process of unknown duration with root as one of the input And once done, add root.quit() at the end.
    def process_of_unknown_duration(root2):
        os.system("python3 EncodeTrain.py")
        messagebox.showinfo("Message","Encoding Completed")
        root2.destroy()

    # Now define our Main Functions, which will first define root, then call for call for "task(root)" --- that's your progressbar, and then call for thread1 simultaneously which will  execute your process_of_unknown_duration and at the end destroy/quit the root.

    def Main():
        root2 = Toplevel()
        t1=threading.Thread(target=process_of_unknown_duration, args=(root2,))
        t1.start()
        task(root2)  # This will block while the mainloop runs
        t1.join()

    #Now just run the functions by calling our Main() function,
    Main()

'''def progress():
    def task(root2):
        root2.mainloop()

    root2 = Toplevel()
    ft = Frame(root2)
    windowWidth = root2.winfo_reqwidth()
    windowHeight = root2.winfo_reqheight()
     
    # Gets both half the screen width/height and window width/height
    positionRight = int(root2.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root2.winfo_screenheight()/2 - windowHeight/2)
    root2.geometry("+{}+{}".format(positionRight, positionDown))
    ft.pack(expand=True, fill=BOTH, side=TOP)
    pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
    pb_hD.pack(expand=True, fill=BOTH, side=TOP)
    pb_hD.start(50)
    root2.after(0,task(root2))
    root2.destroy()'''


def EncFace():
    n=100
    name=e1.get()
    e1.delete(0,'end')
    if all(x.isspace() for x in name):
        messagebox.showerror("Error","Please Enter a Valid Name")    
    elif all(x.isalpha() or x.isspace() for x in name):
        messagebox.showinfo("Message","Take a Photo!")
        os.system("raspistill -w 320 -h 240 -o ./source/newimg.jpg")
        os.system("python3 FaceCrop.py ./source/newimg.jpg")
        if len(os.listdir('./cropped') ) == 0:
            os.system("rm ./cropped/100.jpg")
            messagebox.showinfo("Message","No Face Detected")
        else:
            if(os.path.isdir("./knn_examples/train/"+name)):
                ms=messagebox.askquestion("Message","Face Exists, will append to existing directory, Do you want to Continue?")
                if(ms=='yes'):
                    n+=int(len(os.listdir("./knn_examples/train/"+name)))
                    os.system("mv ./cropped/100.jpg ./cropped/"+str(n)+".jpg")
                    os.system("cp ./cropped/"+str(n)+".jpg ./knn_examples/train/"+name)
                    os.system("rm ./cropped/"+str(n)+".jpg")
                    progress()
                if(ms=='no'):
                    pass
            else:
                os.system("mkdir knn_examples/train/"+name)
                os.system("cp ./cropped/100.jpg ./knn_examples/train/"+name)
                os.system("rm ./cropped/100.jpg")
                progress()
    else:
        messagebox.showerror("Error","Please Enter a Valid Name")
    
        
        

Label(frame, text="Encode Face",font=('Comic Sans MS',20),borderwidth=1, relief="solid").grid(row=0,column=0,columnspan=10,
               rowspan=1,sticky=W+E+N+S, padx=5, pady=5)
#example values
'''for x in range(10):
    for y in range(5):
        btn = Button(frame)
        btn.grid(column=x, row=y, sticky=N+S+E+W)'''
l1=Label(frame, text="Enter Name:",font=('Comic Sans MS',15),borderwidth=1, relief="solid")
l1.grid(row=2,column=2,columnspan=3,sticky=W+E+N+S, padx=5, pady=5)
e1=Entry(frame,font=('Comic Sans MS',15),justify='center')
e1.grid(row=2,column=6,columnspan=2,rowspan=1,sticky=W+E+N+S, padx=5, pady=5)

btn1 = Button(frame,text="Back",font=('Comic Sans MS',15),command=lambda: sys.exit(0))
btn1.grid(column=3, row=4, sticky=N+S+E+W)
btn1 = Button(frame,text="Next",font=('Comic Sans MS',15),command=EncFace)
btn1.grid(column=7, row=4, sticky=N+S+E+W)
'''btn2 = Button(frame,text="Recognition",font=('Comic Sans MS',15),command=RecFace)
btn2.grid(column=5, row=4, sticky=N+S+E+W)
btn3 = Button(frame,text="Surveillance",font=('Comic Sans MS',15),command=EncFace)
btn3.grid(column=8, row=4, sticky=N+S+E+W)'''



for x in range(10):
    Grid.columnconfigure(frame, x, weight=1)

for y in range(5):
    Grid.rowconfigure(frame, y, weight=1)

root.mainloop()
