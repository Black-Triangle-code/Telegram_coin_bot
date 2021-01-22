import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time
import configparser

config = configparser.ConfigParser()
config.read("config.txt")

init()

print(Style.BRIGHT + Fore.YELLOW)
while (True):
	config.set("TCB", "LTCstart", "1")
	config.set("TCB", "DOGEstart", "10")
	with open('config.txt', 'w') as configfile:
    config.write(configfile)
    print("Start LTC")
    processLTC = subprocess.Popen([sys.executable, "bot_LTC.py"])
    print("Start DOGE")
    processDOGE = subprocess.Popen([sys.executable, "bot_DOGE.py"])
    processLTC.wait()
    processDOGE.wait()

    config.set("TCB", "LTCstart", "10")
	config.set("TCB", "DOGEstart", "1")
	with open('config.txt', 'w') as configfile:
    config.write(configfile)
    print("Start LTC")
    processLTC = subprocess.Popen([sys.executable, "bot_LTC.py"])
    print("Start DOGE")
    processDOGE = subprocess.Popen([sys.executable, "bot_DOGE.py"])
    processLTC.wait()
    processDOGE.wait()
