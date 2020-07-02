from tkinter import *
from tkinter import messagebox, simpledialog
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.GUI import TextBox


def login():
    fileKey = open('../FilePassword/key.key', 'rb')
    key = fileKey.read()  # The key will be type bytes
    fileKey.close()

    s = entry.get()
    if(len(key) > 0):
        s = s.replace(" ", "")
        s = s.encode()
        salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        keyInserita = base64.urlsafe_b64encode(kdf.derive(s))

        if(key == keyInserita):
            TextBox.modify(screen)
        else:
            messagebox.showerror('Password Errata', 'La password principale di sistema non corrisponde')
    else:

        string_value = simpledialog.askstring('Non hai ancora una password!', 'Che password di sistema vuoi usare? \nSceglila bene, sarà quella che dovrai usare ogni volta che accesi!',)
        string_value = string_value.replace(" ", "")
        string_value = string_value.encode()
        salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(string_value))
        file = open('key.key', 'wb')
        file.write(key)  # The key is type bytes still
        file.close()

global screen
screen = Tk()
screen.geometry("600x400")
screen.title("Login")
Label(text="Login",  width="500", height="5", font=("Calibri", 40)).pack()
Label(text="Inserisci la password principale:", width="30", height="2", font=("Calibri", 15)).pack()
entry = Entry(text="password", width = "20")
entry.pack()
Label(text = "").pack()
b = Button(text="Login", height="2", width="30", command=login)
b.pack()
screen.mainloop()


