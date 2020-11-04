import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time

init()

print(Style.BRIGHT + Fore.YELLOW)
while (True):
    print("Start LTC")
    processLTC = subprocess.Popen([sys.executable, "bot_LTC.py"])
    processLTC.wait()
    print("Start DOGE")
    processDOGE = subprocess.Popen([sys.executable, "bot_DOGE.py"])
    processDOGE.wait()
