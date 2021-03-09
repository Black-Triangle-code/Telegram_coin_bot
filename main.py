import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time

init()


def console_picture():
    print(Style.BRIGHT + Fore.YELLOW)
    print("Картинки не будет(")
    time.sleep(0.1)


console_picture()

while True:
    choose = input("Нажми 'BOT', 'BALANCE', 'CLIENT', 'DB', 'VIVOD' и Enter чтобы запустить...\n")
    choose = choose.lower()
    if choose == 'bot':
        bot = subprocess.Popen([sys.executable, "bot_V2.py"])
        bot.wait()
        continue
    elif choose == 'balance':
        balance = subprocess.Popen([sys.executable, "balance(exp).py"])
        balance.wait()
        continue
    elif choose == 'client':
        client = subprocess.Popen([sys.executable, "create_client.py"])
        client.wait()
        continue
    elif choose == 'db':
        db = subprocess.Popen([sys.executable, "create_db.py"])
        db.wait()
        continue
    elif choose == 'vivod':
        Vivod = subprocess.Popen([sys.executable, "Vivod.py"])
        Vivod.wait()
        continue
