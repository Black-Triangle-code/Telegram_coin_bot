import sqlite3
import time
from telethon.sync import TelegramClient


with sqlite3.connect('accounts.db') as conn:
    cur = conn.cursor()

    cur.execute("SELECT id, phone, password, api_id, api_hash FROM accounts")
    accounts = cur.fetchall()

    cur.close()

x = 1
total_balance = 0

for x, phone, password, api_id, api_hash in accounts:
    print(f"Входим в аккаунт: {phone}")
    client = TelegramClient(f"anon{x}", api_id, api_hash)
    client.start()

    litecoin_bot = client.get_entity("Litecoin_click_bot")
    
    if client.get_messages(litecoin_bot).total == 0:
        client.send_message(litecoin_bot, "/start")
        time.sleep(1)

    client.send_message(litecoin_bot, "/balance")
    time.sleep(3)
    text = client.get_messages(litecoin_bot, limit=1)[0].message
    balance = float(text.replace('Available balance: ', '').replace(' LTC', ''))
    total_balance += balance
    print(f"Баланс аккаунта № {x} {balance} LTC")

print(f"Общий баланс со всех аккаунтов: {total_balance} LTC")
