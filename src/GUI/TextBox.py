from tkinter import *
from tkinter import messagebox, simpledialog
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def save_file(self):
    print("Save file")

def modify():
    root = Tk()
    root.title("Password")
    text_area = Text()
    text_area.pack(fill=BOTH, expand=1)

    main_menu = Menu()
    root.config(menu=main_menu)
    file_menu = Menu(main_menu)
    main_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save", command=save_file)

