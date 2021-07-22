import subprocess
import sys
import time

from colorama import Fore, Style, init

init()


def console_picture():
    print(Style.BRIGHT + Fore.GREEN)
    print(r"   _____ ________  __________   ___________ ________  ________       ____  ____  ______")
    time.sleep(0.5)
    print(r"  / ___// ____/  |/  / ____/ | / /  _/ ___// ____/ / / / ____/      / __ )/ __ \/_  __/")
    time.sleep(0.5)
    print(r"  \__ \/ __/ / /|_/ / __/ /  |/ // / \__ \/ /   / /_/ / __/        / __  / / / / / /   ")
    time.sleep(0.5)
    print(r" ___/ / /___/ /  / / /___/ /|  // / ___/ / /___/ __  / /___       / /_/ / /_/ / / /    ")
    time.sleep(0.5)
    print(r"/____/_____/_/  /_/_____/_/ |_/___//____/\____/_/ /_/_____/      /_____/\____/ /_/     \n")
    time.sleep(0.5)


console_picture()
print("Нажми Enter чтобы запустить...")
input()

try:
    while True:
        process = subprocess.Popen([sys.executable, "main.py"])
        process.wait()
except KeyboardInterrupt:
    print(Style.BRIGHT + Fore.RED, "--- вы остановили бота ---")
