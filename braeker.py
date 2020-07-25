import winsound
import time
import datetime
import re
import ctypes
import socket
import threading
from ctypes import wintypes

user32 = ctypes.windll.user32
SW_SHOWMAXIMIZED = 3
SW_HIDE = 0
SW_MINIMIZE = 6
keybd_event = ctypes.windll.user32.keybd_event
alt_key = 0x12
extended_key = 0x0001
key_up = 0x0002

HOST = '127.0.0.1'
PORT = 51476
REFRESH_PERIOD = 1

hwnd = user32.GetForegroundWindow()

period = None
start = None
parserPeriod = re.compile(r'(\d+)(\w?)')

showUpInterruption = False

def ListenToConnection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except OSError:
            s.connect((HOST, PORT))
            print(f'Unexpected bind error. Exiting!')
            exit()

        s.listen(2)
        while True:
            conn, addr = s.accept()
            conn.close()
            global showUpInterruption
            showUpInterruption = True


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except OSError as err:
            s.connect((HOST, PORT))
            exit()

    time.sleep(0.5)
    listenerThread = threading.Thread(target=ListenToConnection, daemon=True)
    listenerThread.start()

    while True:
        if not start:
            unparsedPeriod = input(
                f'[{datetime.datetime.now()}] Enter work period; "m" and "h" suffixes supported ->')
            match = parserPeriod.search(unparsedPeriod)
            if not match:
                print('Input is not valid!')
                continue
            value = int(match.group(1))
            suffix = match.group(2)
            coef = 1
            if suffix == 'm':
                coef = 60
            elif suffix == 'h':
                coef = 3600
            period = value*coef
            start = datetime.datetime.now()
            user32.ShowWindow(hwnd, SW_HIDE)
            showUpInterruption = False
        elif (datetime.datetime.now() - start).total_seconds() > period:
            start = None
            showUpInterruption = False
            winsound.PlaySound('brokenGlass.wav',
                               winsound.SND_FILENAME | winsound.SND_ASYNC)
            user32.ShowWindow(hwnd, SW_SHOWMAXIMIZED)
            keybd_event(alt_key, 0, extended_key | 0, 0)
            user32.SetForegroundWindow(hwnd) 
            # Steal focus. Emulating alt key in order to bypass Windows 'security'
            keybd_event(alt_key, 0, extended_key | key_up, 0)
        else:
            time.sleep(REFRESH_PERIOD)
            if showUpInterruption:
                start = None
                user32.ShowWindow(hwnd, SW_SHOWMAXIMIZED)
                showUpInterruption = False
