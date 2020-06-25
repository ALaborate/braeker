import winsound
import time
import datetime
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

hwnd = user32.GetForegroundWindow()

period = None
start = None
if __name__ == '__main__':

    while True:
        if not start:
            period = int(
                input(f'[{datetime.datetime.now()}] Enter work period in seconds ->'))
            start = datetime.datetime.now()
        elif (datetime.datetime.now() - start).total_seconds() > period:
            start = None
            winsound.PlaySound('brokenGlass.wav',
                               winsound.SND_FILENAME | winsound.SND_ASYNC)
            user32.SetForegroundWindow(hwnd)
        else: time.sleep(period)
