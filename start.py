import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time

init()

def console_picture():
    print(Style.BRIGHT + Fore.GREEN)
    print("   _____ ________  __________   ___________ ________  ________       ____  ____  ______")
    time.sleep(0.5)
    print("  / ___// ____/  |/  / ____/ | / /  _/ ___// ____/ / / / ____/      / __ )/ __ \/_  __/")
    time.sleep(0.5)
    print("  \__ \/ __/ / /|_/ / __/ /  |/ // / \__ \/ /   / /_/ / __/        / __  / / / / / /   ")
    time.sleep(0.5)
    print(" ___/ / /___/ /  / / /___/ /|  // / ___/ / /___/ __  / /___       / /_/ / /_/ / / /    ")
    time.sleep(0.5)
    print("/____/_____/_/  /_/_____/_/ |_/___//____/\____/_/ /_/_____/      /_____/\____/ /_/     ")
    time.sleep(0.5)
console_picture()
print("Нажми Enter чтобы запустить...")
input()

while (True):
    process = subprocess.Popen([sys.executable, "bot_V2.py"])
    process.wait()
