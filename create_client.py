from telethon import TelegramClient
import sqlite3
import time

db = sqlite3.connect('account.db')
cur = db.cursor()

cur.execute(f"SELECT COUNT(*) FROM account")
time.sleep(0.1)
h = int(cur.fetchone()[0])
print("Всего записано аккаунтов в БД: " + str(h))

x = h - (h - 1)

while True:
    print("Очередь аккаунта № " + str(x))
    cur.execute(f"SELECT PHONE FROM account WHERE ID = '{x}'")
    time.sleep(0.2)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)
    cur.execute(f"SELECT PASS FROM account WHERE ID = '{x}'")
    time.sleep(0.2)
    password = str(cur.fetchone()[0])
    print("Пароль: " + password)
    cur.execute(f"SELECT API_ID FROM account WHERE ID = '{x}'")
    time.sleep(0.2)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM account WHERE ID = '{x}'")
    time.sleep(0.2)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))
    client = TelegramClient(session, api_id, api_hash)
    client.start()
    print("Аккаунт № " + str(x) + " успешно активирован.")
    time.sleep(1)
    if x == h:
        print("Все аккаунт(ы) активированы!")
        break
    x = x + 1
