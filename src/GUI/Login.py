import base64
import os
import codecs

import yagmail
from tkinter import *
from tkinter import messagebox, simpledialog
from password_generator import PasswordGenerator
from validate_email import validate_email

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from src.GUI import TextBox


def cambia():
    file_key = open('../FilePassword/key.key', 'rb')
    key = file_key.read()  # The key will be type bytes
    file_key.close()

    if len(key) > 0:
        answer = messagebox.askyesno("Se continui perderai le vecchie password", "Vuoi continuare?")
        if answer is None:
            return
        else:
            modifica_password()
    else:
        modifica_password()


def calcola_key(s):
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
    return base64.urlsafe_b64encode(kdf.derive(s))


def login():
    file_key = open('../FilePassword/key.key', 'rb')
    key = file_key.read()  # The key will be type bytes
    file_key.close()

    s = entry.get()
    if len(key) > 0:
        key_inserita = calcola_key(s)

        if key == key_inserita:
            TextBox.modify(screen)
        else:
            messagebox.showerror('Password Errata', 'La password principale di sistema non corrisponde')
    else:
        cambia()


def prendi_messaggio():
    file_testo = "../FilePassword/AllPasswords.encrypted"
    decrypted = ""

    with open(file_testo, 'rb') as f:
        encrypt = f.read()
    if len(encrypt) > 0:
        file_chiave = open("../FilePassword/key.key", "rb")
        key = file_chiave.read()  # The key will be type bytes
        file_chiave.close()

        f = Fernet(key)
        decrypted = f.decrypt(encrypt)
    return decrypted


def cripta_messaggio(msg, key):
    return Fernet(key).encrypt(bytes(msg, encoding="utf-8"))


def manda_mail(messaggio_criptato, key, indirizzo_mail):
    yag = yagmail.SMTP('indirizzoemail', 'password')
    # TODO: sto correntemente usando il mio indirizzo privato, bisogna crearne uno gmail dedicato
    content = 'Ciao, stai ricevendo questa mail in quanto hai deciso di resettare il tuo client password\n' \
              + '\nLa tua chiave è: ' + str(key, encoding="utf-8") \
              + '\n\nQua trovi il testo criptato contenente le tue password\n' + str(messaggio_criptato,
                                                                                     encoding="utf-8")
    contenuto = [content]
    yag.send(indirizzo_mail.decode("utf-8"), 'Client password: reset', contenuto)
    yag.close()


def reset_manda_mail():
    if os.path.exists('../FilePassword/mailaddress.key'):
        file = open('../FilePassword/mailaddress.key', 'rb')
        filepwd = open('../FilePassword/Fernet.key', 'rb')

        indirizzo_mail = Fernet(filepwd.read()).decrypt(file.read())
        pwd = Fernet.generate_key()
        msg = prendi_messaggio()
        k_msg = cripta_messaggio(msg, pwd)
        print(k_msg, indirizzo_mail)
        manda_mail(k_msg, pwd, indirizzo_mail)
        filepwd.close()
    else:
        file = open('../FilePassword/Fernet.key', 'wb')
        file.write(Fernet.generate_key())
    file.close()


def modifica_password():
    string_value = simpledialog.askstring('Modifica la password!',
                                          'Che password di sistema vuoi usare? \nSceglila bene, sarà quella che '
                                          'dovrai usare ogni volta che accedi!')
    indirizzo_mail = simpledialog.askstring('Inserisci mail di recupero',
                                            'Inserisci la mail di recupero, questa ti sarà utile per recuperare le '
                                            'tue password!')

    if len(string_value) > 0:
        key = calcola_key(string_value)
        file = open('../FilePassword/key.key', 'wb')
        file.write(key)
        file.close()

        file_testo = "../FilePassword/AllPasswords.encrypted"

        open(file_testo, 'w').close()

    if len(indirizzo_mail) > 0 and validate_email(indirizzo_mail):
        reset_manda_mail()
        filepwd = open('../FilePassword/Fernet.key', 'rb')
        enc = Fernet(filepwd.read()).encrypt(bytes(indirizzo_mail, encoding="utf-8"))
        file = open('../FilePassword/mailaddress.key', 'wb')
        file.write(enc)
        file.close()
        filepwd.close()


global screen
screen = Tk()
screen.geometry("600x600")
screen.title("Login")
Label(text="Login", width="500", height="5", font=("Calibri", 40)).pack()
Label(text="Inserisci la password principale:", width="30", height="2", font=("Calibri", 15)).pack()
entry = Entry(text="password", width="20")
entry.pack()
Label(text="").pack()
b = Button(text="Login", height="2", width="30", command=login)
b.pack()
cambiaBtn = Button(text="Cambia Password", height="2", width="30", command=cambia)
cambiaBtn.pack()
if __name__ == '__main__':
    screen.mainloop()
