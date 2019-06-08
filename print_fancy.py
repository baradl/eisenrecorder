"""
Script for art at the beginning of each start of the Eisenrecorder
"""

import sys
#import textwrap
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected ---
from termcolor import cprint 
from pyfiglet import figlet_format
import os

from ctypes import windll, byref,wintypes

#os.system("mode con cols=79 lines=43")


STDOUT = -11


hdl = windll.kernel32.GetStdHandle(STDOUT)
rect = wintypes.SMALL_RECT(0, 50, 90, 180) # (left, top, right, bottom)
windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))

bufsize = wintypes._COORD(1000, 100) # rows, columns
windll.kernel32.SetConsoleScreenBufferSize(bufsize)

cprint(figlet_format('  EISENRECORDER  ', font='standard'), 'white', 'on_red', 
       attrs=(['underline','bold', 'dark']))

with open("barbell_ascii.txt") as bb:
    print(bb.read())
        
