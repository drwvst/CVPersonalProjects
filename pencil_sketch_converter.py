import cv2 # OpenCV library
import numpy as np # Scientific computing
import tkinter as tk # Standard GUI toolKit
from tkinter import filedialog #provides dialogs for opening or saving files
from tkinter import messagebox # simple pop-up message windows for info, warnings, and errors
from PIL import Image,ImageTk # Image is uesd to open, manipulate, and save images
# ImageTk is a module to convert Pillow images into a format for the GUI to understand

images = {"original" : None, "sketch" : None}


def open_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    img = cv2.imread(filepath)
    display_image(img, original = True)
    sketch_img() = convert_to_sketch(img)
    display_image(sketch_img, original = False)


def convert_to_sketch(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # cvtColor means "convert color" --> (image, conversion code)
    inverted_img = cv2.bitwise_not(gray_img) # color inversion
    blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), sigmaX=0, sigmaY=0)
    # ^^ Makes every pixel the weighted average of its surrounding pixels
    # softens edges and reduces noise. (image, kernel size, stdevation x dir, std y dir)
    inverted_blur_img = cv2.bitwise_not(blurred_img) # invert blurred image back
    sketch_img = cv2.divide(gray_img, inverted_blur_img, scale=256.0)
    return sketch_img


def display_image(img, original):