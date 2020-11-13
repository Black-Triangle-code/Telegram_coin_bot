import sqlite3
import time
from telethon import TelegramClient
from telethon import sync, events
import re
import json
import configparser

config = configparser.ConfigParser()
config.read("config.txt")
maxbot = config["TCB"]["maxbot"]

db = sqlite3.connect('Account.db')
cur = db.cursor()

x = 1

while(True):
    if x == maxbot:
        
        print("Конец")
        break
    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)

    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))
    client = TelegramClient(session, api_id, api_hash)
    client.start()

    dlgs = client.get_dialogs()
    for dlg in dlgs:
        if dlg.title == 'LTC Click Bot':
            tegmo = dlg

    client.send_message('LTC Click Bot', "/balance")
    time.sleep(3)
    msgs = client.get_messages(tegmo, limit=1)

    for mes in msgs:
        str_a = str(mes.message)
        zz = str_a.replace('Available balance: ', '')
        qq = zz.replace(' LTC', '')
        print(qq)
        waitin = float(qq)

        if waitin >= 0.0004:
            client.send_message('LTC Click Bot', "💵 Withdraw")
            time.sleep(3)
            cur.execute(f"SELECT LTC FROM Account WHERE ID = '{x}'")
            time.sleep(0.4)
            litecoin = str(cur.fetchone()[0])
            client.send_message('LTC Click Bot', litecoin)
            Adolf = round(waitin, 5)
            Eva = float(Adolf) - 0.00001
            vivod = float(Eva)
            print("Выводим: " + str(vivod) + " LTC")
            time.sleep(3)
            client.send_message('LTC Click Bot', str(vivod))
            time.sleep(3)
            client.send_message('LTC Click Bot', "✅ Confirm")
            time.sleep(3)
            client.send_message('LTC Click Bot', "🏠 Menu")
            time.sleep(3)
            
            #----------------------------------------------------------------
            
            dlgs = client.get_dialogs()
    for dlg in dlgs:
        if dlg.title == 'DOGE Click Bot':
            tegmo = dlg

    client.send_message('DOGE Click Bot', "/balance")
    time.sleep(3)
    msgs = client.get_messages(tegmo, limit=1)

    for mes in msgs:
        str_a = str(mes.message)
        zz = str_a.replace('Available balance: ', '')
        qq = zz.replace(' DOGE', '')
        print(qq)
        waitin = float(qq)

        if waitin >= 4:
            client.send_message('DOGE Click Bot', "💵 Withdraw")
            time.sleep(3)
            cur.execute(f"SELECT DOGE FROM Account WHERE ID = '{x}'")
            time.sleep(0.4)
            dogecoin = str(cur.fetchone()[0])
            client.send_message('DOGE Click Bot', dogecoin)
            Adolf = round(waitin, 5)
            Eva = float(Adolf) - 0.1
            vivod = float(Eva)
            print("Выводим: " + str(vivod) + " DOGE")
            time.sleep(3)
            client.send_message('DOGE Click Bot', str(vivod))
            time.sleep(3)
            client.send_message('DOGE Click Bot', "✅ Confirm")
            time.sleep(3)
            client.send_message('DOGE Click Bot', "🏠 Menu")
            time.sleep(3)

    x = x + 1
    time.sleep(1)
