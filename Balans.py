import sqlite3
import time
from telethon import TelegramClient
from telethon import sync, events
import re
import json


db = sqlite3.connect('Account.db')
cur = db.cursor()

x = 1
m = 0

while(True):
    if x == 23:
        print("Готово!")
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

    m = m + waitin
    print(m)
    x = x + 1
    time.sleep(1)
