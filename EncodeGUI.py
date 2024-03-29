from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import os,os.path
import sys
import dlib
from PIL import Image
import threading

# Declare Tkinter Root widget and child Frame widget
root = Tk()
frame=Frame(root)

# Set dimensions and orientation of window
width, height = frame.winfo_screenwidth(), frame.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width,height))
root.attributes("-fullscreen",True)

# Configure Grid View of Frame
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

    # Now define our Main Functions, which will first define root, then call for call for "task(root)" --- that's your progressbar, and then call for thread1 simultaneously which will execute your process_of_unknown_duration and at the end destroy/quit the root.
    def Main():
        root2 = Toplevel()
        t1=threading.Thread(target=process_of_unknown_duration, args=(root2,))
        t1.start()
        task(root2)  # This will block while the mainloop runs
        t1.join()

    # Now just run the functions by calling our Main() function,
    Main()

def EncFace():
    # Get name of Person to be added
    images_count=100
    name=name_entry_field.get()
    name_entry_field.delete(0,'end')

    # Check if name is Valid
    if all(x.isspace() for x in name):
        messagebox.showerror("Error","Please Enter a Valid Name")    
    elif all(x.isalpha() or x.isspace() for x in name):
        messagebox.showinfo("Message","Take a Photo!")

        # Take Photo using inbuilt raspistill module
        os.system("raspistill -w 320 -h 240 -o ./source/newimg.jpg")
        os.system("python3 FaceCrop.py ./source/newimg.jpg")

        # Check if face is detected in taken picture
        if len(os.listdir('./cropped') ) == 0:
            os.system("rm ./cropped/100.jpg")
            messagebox.showinfo("Message","No Face Detected")

        else:
            # Check if person already present in the system
            if(os.path.isdir("./Faces_train_dir/train/"+name)):
                ms=messagebox.askquestion("Message","Face Exists, will append to existing directory, Do you want to Continue?")

                # Place photo in person's directory
                if(ms=='yes'):
                    images_count+=int(len(os.listdir("./Faces_train_dir/train/"+name)))
                    os.system("mv ./cropped/100.jpg ./cropped/"+str(images_count)+".jpg")
                    os.system("cp ./cropped/"+str(images_count)+".jpg ./Faces_train_dir/train/"+name)
                    os.system("rm ./cropped/"+str(images_count)+".jpg")
                    progress()
                if(ms=='no'):
                    pass
            else:
                os.system("mkdir Faces_train_dir/train/"+name)
                os.system("cp ./cropped/100.jpg ./Faces_train_dir/train/"+name)
                os.system("rm ./cropped/100.jpg")
                progress()
    else:
        messagebox.showerror("Error","Please Enter a Valid Name")


# Declare label and button widgets
Label(frame, text="Encode Face",font=('Comic Sans MS',20),borderwidth=1, relief="solid").grid(row=0,column=0,columnspan=10,
               rowspan=1,sticky=W+E+N+S, padx=5, pady=5)

l1=Label(frame, text="Enter Name:",font=('Comic Sans MS',15),borderwidth=1, relief="solid")
l1.grid(row=2,column=2,columnspan=3,sticky=W+E+N+S, padx=5, pady=5)
name_entry_field=Entry(frame,font=('Comic Sans MS',15),justify='center')
name_entry_field.grid(row=2,column=6,columnspan=2,rowspan=1,sticky=W+E+N+S, padx=5, pady=5)

btn1 = Button(frame,text="Back",font=('Comic Sans MS',15),command=lambda: sys.exit(0))
btn1.grid(column=3, row=4, sticky=N+S+E+W)
btn1 = Button(frame,text="Next",font=('Comic Sans MS',15),command=EncFace)
btn1.grid(column=7, row=4, sticky=N+S+E+W)

for x in range(10):
    Grid.columnconfigure(frame, x, weight=1)

for y in range(5):
    Grid.rowconfigure(frame, y, weight=1)

root.mainloop()
