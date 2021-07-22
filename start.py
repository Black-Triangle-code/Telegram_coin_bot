import subprocess
import sys
import time

from colorama import Fore, Style, init


init()


def console_picture():
    print(Style.BRIGHT + Fore.YELLOW)
    print(r"  _____          _                           _            ____            _   ")
    time.sleep(0.5)
    print(r" |_   _|  _ __  (_)   __ _   _ __     __ _  | |   ___    | __ )    ___   | |_ ")
    time.sleep(0.5)
    print(r"   | |   | '__| | |  / _` | | '_ \   / _` | | |  / _ \   |  _ \   / _ \  | __|")
    time.sleep(0.5)
    print(r"   |_|   |_|    |_|  \__,_| |_| |_|  \__, | |_|  \___|   |____/   \___/   \__|")
    time.sleep(0.5)
    print(r"                                     |___/                                    ")
    time.sleep(0.5)


try:
    console_picture()
    input("Нажми Enter чтобы запустить...")
    while True:
        process = subprocess.Popen([sys.executable, "main.py"])
        process.wait()
except KeyboardInterrupt:
    print(Style.BRIGHT + Fore.RED, "--- вы остановили бота ---")
