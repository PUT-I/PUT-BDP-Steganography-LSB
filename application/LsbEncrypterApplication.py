"""Contains implementation of Lsb encrypter application"""

import os
import tkinter as tk
from math import floor
from tkinter import messagebox

import cv2

from application.LsbEncrypter import LsbEncrypter


class LsbEncrypterApplication(tk.Frame):
    """Application for LSB encryption"""

    text: str
    bit_position: int

    def __init__(self, master=None):
        self.img = None
        self.img_encryption = None
        self.text = ''
        self.bit_position = 0
        self.available_bytes = 0
        super().__init__(master)
        self.master = master
        self.pack()
        self._create_widgets()

    def _create_widgets(self):
        self.image_filename_frame = tk.LabelFrame(self, text="Image filename")
        self.image_filename_frame.pack(fill='x', expand=True)
        self.image_filename_input = tk.Entry(self.image_filename_frame, bd=5)
        self.image_filename_input.pack(fill='x', expand=True)

        self.loaded_image_filename_frame = tk.LabelFrame(self, text="Loaded image filename")
        self.loaded_image_filename_frame.pack(fill='x', expand=True)
        self.loaded_image_filename_input = tk.Entry(self.loaded_image_filename_frame, bd=5)
        self.loaded_image_filename_input.pack(fill='x', expand=True)
        self.loaded_image_filename_input.insert(tk.END, "Image not loaded")
        self.loaded_image_filename_input.configure(state='disabled')

        self.max_bits_frame = tk.LabelFrame(self, text="Amount of bits available")
        self.max_bits_frame.pack(fill='x', expand=True)
        self.max_bits_input = tk.Entry(self.max_bits_frame, bd=5)
        self.max_bits_input.pack(fill='x', expand=True)
        self.max_bits_input.insert(tk.END, "Image not loaded")
        self.max_bits_input.configure(state='disabled')

        self.text_filename_frame = tk.LabelFrame(self, text="Text filename")
        self.text_filename_frame.pack(fill='x', expand=True)
        self.text_filename_input = tk.Entry(self.text_filename_frame, bd=5)
        self.text_filename_input.pack(fill='x', expand=True)

        self.load_file_button = tk.Button(self)
        self.load_file_button["text"] = "Load image"
        self.load_file_button["command"] = self._load_image
        self.load_file_button.pack()

        self.encryption_button = tk.Button(self)
        self.encryption_button["text"] = "Bit encryption"
        self.encryption_button["command"] = self._bit_encryption
        self.encryption_button.pack()

    def _load_image(self):
        image_filename: str = self.image_filename_input.get()

        if len(image_filename) == 0:
            messagebox.showinfo("Error", "Enter image filename!")
            return
        elif not os.path.exists(image_filename) or not os.path.isfile(image_filename):
            messagebox.showinfo("Error", "Image file does not exists!")
            return

        self.img = cv2.imread(image_filename)

        if len(self.img.shape) == 2:
            self.available_bytes = floor((self.img.shape[0] * self.img.shape[1]) / 8) - 1
        elif len(self.img.shape) == 3:
            self.available_bytes = floor((self.img.shape[0] * self.img.shape[1] * self.img.shape[2]) / 8) - 1

        self.max_bits_input.configure(state='normal')
        self.max_bits_input.delete('0', tk.END)
        self.max_bits_input.insert(tk.END, str(self.available_bytes) + " bytes")
        self.max_bits_input.configure(state='disabled')

        self.loaded_image_filename_input.configure(state='normal')
        self.loaded_image_filename_input.delete('0', tk.END)
        self.loaded_image_filename_input.insert(tk.END, image_filename)
        self.loaded_image_filename_input.configure(state='disabled')

    def _load_text_file(self):
        text_filename: str = self.text_filename_input.get()

        if len(text_filename) == 0:
            messagebox.showinfo("Error", "Enter text filename!")
            return None
        elif not os.path.exists(text_filename) or not os.path.isfile(text_filename):
            messagebox.showinfo("Error", "Text file does not exists!")
            return None

        file = open(text_filename, 'r', encoding="utf8", errors='ignore')
        self.text = file.read()
        file.close()
        return not None

    def _bit_encryption_callback(self, value: int):
        self.bit_position = value

    def _show_encryption_image(self, window_title: str, img):
        if img.shape[1] >= 512:
            cv2.imshow(window_title, img)
        else:
            border_size: int = 256 - floor(img.shape[1] / 2)
            img_copy = img.copy()
            img_copy = cv2.copyMakeBorder(img_copy, 0, 0, border_size, border_size, cv2.BORDER_CONSTANT)
            cv2.imshow(window_title, img_copy)

    def _bit_encryption(self):
        if self.img is None:
            messagebox.showinfo("Error", "Load image and input text filename first!")
            return

        if self._load_text_file() is None:
            return

        if len(self.text) > self.available_bytes:
            messagebox.showinfo("Warning", "Too long text! Text will be cropped to fit into image.")

        window_title: str = 'Bit encryption'

        cv2.namedWindow(window_title)
        cv2.createTrackbar('Bit pos', window_title, 0, 8, self._bit_encryption_callback)
        self._show_encryption_image(window_title, self.img)

        key = ord('a')
        while key != ord('q') and cv2.getWindowProperty(window_title, cv2.WND_PROP_VISIBLE) >= 1:
            key = cv2.waitKey(50)
            if key == ord('s'):
                self.img_encryption = LsbEncrypter.encrypt(self.img, self.text, self.bit_position)
                self._show_encryption_image(window_title, self.img_encryption)

        image_filename: list = self.image_filename_input.get().split('.')
        new_image_filename: str = image_filename[0] + "_encrypted." + image_filename[1]

        if self.img_encryption is not None and (self.img_encryption - self.img).sum() != 0:
            cv2.imwrite(new_image_filename, self.img_encryption)
            self.img_encryption = None
        cv2.destroyWindow(window_title)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Modified LSB encrypter")
    app = LsbEncrypterApplication(master=root)
    app.mainloop()
