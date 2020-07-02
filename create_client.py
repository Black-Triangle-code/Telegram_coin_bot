from telethon import TelegramClient
import sqlite3
import time

db = sqlite3.connect('Account.db')
cur = db.cursor()

x = 1

while(True):
    print("Очередь аккаунта № " + str(x))
    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
    time.sleep(0.2)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)
    cur.execute(f"SELECT PASS FROM Account WHERE ID = '{x}'")
    time.sleep(0.2)
    password = str(cur.fetchone()[0])
    print(password)
    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
    time.sleep(0.2)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
    time.sleep(0.2)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))
    client = TelegramClient(session, api_id, api_hash)
    client.start()
    x = x + 1
    time.sleep(1)
    if x == 32:
        print("Aккаунты активированы!")
        break
