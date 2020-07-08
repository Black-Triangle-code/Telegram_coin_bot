from telethon.sync import TelegramClient
import sqlite3

with sqlite3.connect('accounts.db') as conn:
    cur = conn.cursor()

    cur.execute("SELECT id, phone, password, api_id, api_hash FROM accounts")
    accounts = cur.fetchall()

    cur.close()


for x, phone, password, api_id, api_hash in accounts:
    print(f"Очередь аккаунта № {x}\n"
          f"Входим в аккаунт: {phone}")
    session = f"anon{x}"
    client = TelegramClient(session, api_id, api_hash)
    client.start(phone, password=password)


print("Аккаунты активированы!")
