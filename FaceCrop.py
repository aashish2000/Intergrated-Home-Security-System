import sys
import time
import dlib
import matplotlib.pyplot as plt
import PIL.Image
from tkinter import *

output_dir="cropped"
detector = dlib.get_frontal_face_detector()
win = dlib.image_window()

img_to_be_cropped=sys.argv[1]
img = dlib.load_rgb_image(img_to_be_cropped)

# Run Dlib's face detector
dets = detector(img, 1)
if(len(dets)==0):
    messagebox("Error","Face not found, Try again")
    sys.exit(0)

# Crop Image
for i, d in enumerate(dets):    
    cropped_image = PIL.Image.open(img_to_be_cropped)
    cropped_image.save(output_dir + "/" + str("100") + ".jpg", "JPEG")

# Display cropped image
win.clear_overlay()
win.set_image(img)
win.add_overlay(dets)
time.sleep(5)
win.clear_overlay()

    
    
