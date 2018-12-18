import sys
import time
import dlib
import matplotlib.pyplot as plt
import PIL.Image
from tkinter import *

crop_width=108
put_dirname="cropped"
detector = dlib.get_frontal_face_detector()
win = dlib.image_window()

f=sys.argv[1]
print("Processing file: {}".format(f))
img = dlib.load_rgb_image(f)
# The 1 in the second argument indicates that we should upsample the image
# 1 time.  This will make everything bigger and allow us to detect more
# faces.
dets = detector(img, 1)
print("Number of faces detected: {}".format(len(dets)))
if(len(dets)==0):
    messagebox("Error","Face not found, Try again")
    sys.exit(0)
for i, d in enumerate(dets):
    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        i, d.left(), d.top(), d.right(), d.bottom()))
    '''width = d.right() - d.left()
    height = d.bottom() - d.top()
    if width >= crop_width and height >= crop_width:'''
    print("crop")
    #image_to_crop = PIL.Image.open(f)
    cropped_image = PIL.Image.open(f)
    #crop_area = (d.left(), d.top(), d.right(), d.bottom())
    #cropped_image = image_to_crop.crop(crop_area)
    cropped_image.save(put_dirname + "/" + str("100") + ".jpg", "JPEG")
    print("crop2")

win.clear_overlay()
win.set_image(img)
win.add_overlay(dets)
time.sleep(5)
win.clear_overlay()

    
    
