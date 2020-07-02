from tkinter import *

from cryptography.fernet import Fernet


def addAll(text):
    file_testo = "../FilePassword/AllPasswords.encrypted"
    output_file = "../FilePassword/Decifrate.txt"
    with open(file_testo, 'rb') as f:
        encrypt = f.read()

    if len(encrypt) > 0:
        file_chiave = open("../FilePassword/key.key", "rb")
        key = file_chiave.read()  # The key will be type bytes
        file_chiave.close()

        f = Fernet(key)
        decrypted = f.decrypt(encrypt)

        with open(output_file, 'wb') as f:
            f.write(decrypted)

        file_finale = open("../FilePassword/Decifrate.txt", "r")
        lines = file_finale.readlines()

        for i in range(len(lines)):
            text.insert(END, lines[i])

        file_finale.close()


def save():
    t = text.get("1.0", "end-1c")
    if (len(t)) > 0:
        input_file = '../FilePassword/Decifrate.txt'
        output_file = '../FilePassword/AllPasswords.encrypted'

        with open(input_file, 'w') as f:
            f.write(t)

        with open(input_file, 'rb') as f:
            data = f.read()

        file_chiave = open("../FilePassword/key.key", "rb")
        key = file_chiave.read()  # The key will be type bytes
        file_chiave.close()

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
    Label(root, text="").pack()
    root.mainloop()
