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
    sketch_img = convert_to_sketch(img)
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
    max_size = (400, 400)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if original else img
    img_pil = Image.fromarray(img_rgb)

    img_pil.thumbnail(max_size)

    img_tk = ImageTk.PhotoImage(image=img_pil)

    if original:
        images["original"] = img_pil
    else:
        images["sketch"] = img_pil

    label = original_image_label if original else sketch_image_label
    label.config(image=img_tk)
    label.image = img_tk


def save_sketch():
    if images["sketch"] is None:
        messagebox.showerror("Error", "No Sketch to save.")
        return

    sketch_filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not sketch_filepath:
        return

    images["sketch"].save(sketch_filepath, "PNG")
    messagebox.showinfo("Saved", "Sketch saved to {}".format(sketch_filepath))


app = tk.Tk()
app.title('Pencil Sketch Converter')
frame = tk.Frame(app)
frame.pack(pady=10, padx=10)

original_image_label = tk.Label(frame)
original_image_label.grid(row=0, column=0, padx=5, pady=5)
sketch_image_label = tk.Label(frame)
sketch_image_label.grid(row=0, column=1, padx=5, pady=5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

open_button = tk.Button(btn_frame, text="Open Image", command=open_file)
open_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(btn_frame, text="Save Sketch", command=save_sketch)
save_button.grid(row=0, column=1, padx=5)

app.mainloop()
