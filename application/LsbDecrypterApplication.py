"""Contains implementation Lsb decrypter application"""

import os
import tkinter as tk
from tkinter import messagebox

import cv2

from application.LsbEncrypter import LsbEncrypter


class LsbDecrypterApplication(tk.Frame):
    """Application for LSB decryption"""

    def __init__(self, master=None):
        self.img = None
        super().__init__(master)
        self.master = master
        self.pack()
        self._create_widgets()

    def _create_widgets(self):
        self.image_filename_frame = tk.LabelFrame(self, text="Image filename")
        self.image_filename_frame.pack(fill='x', expand=True)
        self.image_filename_input = tk.Entry(self.image_filename_frame, bd=5)
        self.image_filename_input.pack(fill='x', expand=True)

        self.bit_position_frame = tk.LabelFrame(self, text="Bit position (1-8)")
        self.bit_position_frame.pack(fill='x', expand=True)
        self.bit_position_input = tk.Entry(self.bit_position_frame, bd=5)
        self.bit_position_input.pack(fill='x', expand=True)

        self.decryption_button = tk.Button(self)
        self.decryption_button["text"] = "Decrypt"
        self.decryption_button["command"] = self._bit_decryption
        self.decryption_button.pack()

        self.text_frame = tk.LabelFrame(text="Decrypted text")
        self.text_frame.pack(fill='x', expand=True)
        self.text_text_area = tk.Text(self.text_frame, state='disabled', height=40)
        self.text_text_area.pack(fill='x', expand=True)

    def _load_image(self):
        image_filename: str = self.image_filename_input.get()

        if len(image_filename) == 0:
            return
        elif not os.path.exists(image_filename) or not os.path.isfile(image_filename):
            return

        self.img = cv2.imread(image_filename)

    def _bit_decryption(self):
        self._load_image()

        if self.img is None:
            messagebox.showinfo("Error", "File does not exist!")
            return

        if 0 > int(self.bit_position_input.get()) < 8:
            messagebox.showinfo("Error", "Enter correct bit position!")
            return

        bit_position: int = int(self.bit_position_input.get())
        text: str = LsbEncrypter.decrypt(self.img, bit_position)
        self.text_text_area.configure(state='normal')
        self.text_text_area.delete('1.0', tk.END)
        self.text_text_area.insert(tk.END, text)
        self.text_text_area.configure(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Modified LSB decrypter")
    app = LsbDecrypterApplication(master=root)
    app.mainloop()
