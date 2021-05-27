import sqlite3
import time

from telethon import TelegramClient

db = sqlite3.connect('Account.db')
cur = db.cursor()

num = 1

while True:
    print("Очередь аккаунта № " + str(num))
    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{num}'")
    time.sleep(0.2)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)
    cur.execute(f"SELECT PASS FROM Account WHERE ID = '{num}'")
    time.sleep(0.2)
    password = str(cur.fetchone()[0])
    print(password)
    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{num}'")
    time.sleep(0.2)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{num}'")
    time.sleep(0.2)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(num))
    client = TelegramClient(session, api_id, api_hash)
    client.start()
    num = num + 1
    time.sleep(1)
    if num == 32:
        print("Aккаунты активированы!")
        break
