import winsound
import time
import datetime
import re
import ctypes
import socket
import threading
from os.path import isfile
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
HELP_STRING = '''
This program is designed to serve as trigger that notifies the user \
that its time to stand up, leave workstation and have some rest.

Basic idea is that you print how many time you plan to work, console window disappears and shows up after the time passed. \
If you need to interrupt program just run another instance.

Examples of accepted inputs (no quotes)
"120" - 120 seconds
"15m" - 15 minutes
"2h" - 2 hours
"q" - show stats and quit
"?" - display this help
'''

hwnd = user32.GetForegroundWindow()

period = None
start = None
parserPeriod = re.compile(r'(\d+)(\w?)')

showUpInterruption = False
workTime = datetime.datetime.now() - datetime.datetime.now()


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
            conn = s.accept()[0]
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

    def Interrupt():
        global start
        global showUpInterruption
        global workTime
        workTime = workTime + (datetime.datetime.now() - start)
        start = None
        showUpInterruption = False
        user32.ShowWindow(hwnd, SW_SHOWMAXIMIZED)
        keybd_event(alt_key, 0, extended_key | 0, 0)
        user32.SetForegroundWindow(hwnd)
        # Steal focus. Emulating alt key in order to bypass Windows 'security'
        keybd_event(alt_key, 0, extended_key | key_up, 0)

    while True:
        if not start:
            unparsedPeriod = input(
                f'[{datetime.datetime.now()}] $ ')
            if 'q' in unparsedPeriod:
                break
            if '?' in unparsedPeriod:
                print(HELP_STRING)
                continue
            match = parserPeriod.search(unparsedPeriod)
            if not match:
                print('Input is not valid! Type "?" for help. ')
                continue
            value = int(match.group(1))
            suffix = match.group(2)
            coef = 1
            if suffix == 'm' or suffix == 'м':
                coef = 60
            elif suffix == 'h' or suffix == 'ч':
                coef = 3600
            period = value*coef
            start = datetime.datetime.now()
            user32.ShowWindow(hwnd, SW_HIDE)
            showUpInterruption = False
        elif (datetime.datetime.now() - start).total_seconds() > period:
            if isfile('brokenGlass.wav'):
                winsound.PlaySound('brokenGlass.wav',
                               winsound.SND_FILENAME | winsound.SND_ASYNC)
            Interrupt()
        else:
            time.sleep(REFRESH_PERIOD)
            if showUpInterruption:
                Interrupt()

    mikes = workTime.total_seconds()/60
    hours = workTime.total_seconds()/3600
    input(f'\nTotal worktime: {mikes:.1f} minutes, or approximately {hours:.1f} hours\nPress Enter to exit.')
