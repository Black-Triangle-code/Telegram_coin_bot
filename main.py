import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time
import psutil
from subprocess import check_output, CalledProcessError

def getPIDs(process):
       try:
           pidlist = map(int, check_output(["pidof", process]).split())
       except  CalledProcessError:
           pidlist = []
       print ('list of PIDs = ' + ', '.join(str(e) for e in pidlist))
       return pidlist

print(Style.BRIGHT + Fore.YELLOW)
while (True):
    pid1 = getPIDs("/usr/bin/python3 bot_DOGE.py")
    pid2 = getPIDs("/usr/bin/python3 control.py")
    pid3 = getPIDs("/usr/bin/python3 bot_LTC.py")
    for p in pid1:
        psutil.Process(p).terminate()
    for p in pid2:
        psutil.Process(p).terminate()
    for p in pid3:
        psutil.Process(p).terminate()

    process = subprocess.Popen([sys.executable, "control.py"])
    process.wait()
