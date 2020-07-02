from tkinter import *
from tkinter import messagebox, simpledialog
import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from tkinter import *



def addAll(text):
    fileTesto = "../FilePassword/AllPasswords.encrypted"
    output_file = "../FilePassword/Decifrate.txt"
    with open(fileTesto, 'rb') as f:
        encrypt = f.read()

    if(len(encrypt)>0):
        fileChiave = open("../FilePassword/key.key", "rb")
        key = fileChiave.read()  # The key will be type bytes
        fileChiave.close()

        f = Fernet(key)
        decrypted = f.decrypt(encrypt)

        with open(output_file, 'wb') as f:
            f.write(decrypted)

        fileFinale = open("../FilePassword/Decifrate.txt", "r")
        lines = fileFinale.readlines()

        for i in range(len(lines)):
            text.insert(END, lines[i])

        fileFinale.close()



def save():
    t = text.get("1.0", "end-1c")
    if(len(t))>0:

        input_file = '../FilePassword/Decifrate.txt'
        output_file = '../FilePassword/AllPasswords.encrypted'

        with open(input_file, 'w') as f:
            f.write(t)

        with open(input_file, 'rb') as f:
            data = f.read()

        fileChiave = open("../FilePassword/key.key", "rb")
        key = fileChiave.read()  # The key will be type bytes
        fileChiave.close()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

        with open(input_file, 'w') as f:
            f.write("nulla")

    root.destroy()


def modify(screen):
    global root
    global text
    root = Toplevel(screen)
    root.title("Password Editor")
    text = Text(root)
    addAll(text)
    text.pack()
    Label(root, text="").pack()
    button = Button(root, text="Salva", command=save)
    button.pack()
    Label(root,text="").pack()
    root.mainloop()


