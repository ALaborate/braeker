import winsound
import time
import datetime
import re
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
SW_SHOWMAXIMIZED = 3
SW_HIDE = 0
SW_MINIMIZE = 6

hwnd = user32.GetForegroundWindow()

period = None
start = None
parserPeriod = re.compile(r'(\d+)(\w?)')
if __name__ == '__main__':

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
            user32.ShowWindow(hwnd, SW_MINIMIZE)
        elif (datetime.datetime.now() - start).total_seconds() > period:
            start = None
            winsound.PlaySound('brokenGlass.wav',
                               winsound.SND_FILENAME | winsound.SND_ASYNC)
            user32.ShowWindow(hwnd, SW_SHOWMAXIMIZED)
        else:
            time.sleep(period)
