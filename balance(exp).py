import sqlite3
import time
from telethon import TelegramClient
from telethon import sync, events
import re
import json
import dictionary as d


def login(x):
    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
    time.sleep(0.1)
    global Phone
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)
    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
    time.sleep(0.1)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
    time.sleep(0.1)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))
    global client
    client = TelegramClient(session, api_id, api_hash)
    client.start()


def balance(bot, client):
    global num
    COIN_name = d.coin[bot]['bot']
    dlgs = client.get_dialogs()
    for dlg in dlgs:
        if dlg.title == COIN_name:
            tegmo = dlg

    client.send_message(COIN_name, "/balance")
    time.sleep(1)
    msgs = client.get_messages(tegmo, limit=1)

    currency = d.coin[bot][d.currency]

    for mes in msgs:
        str_a = str(mes.message)
        qq = str_a.replace('Available balance: ', '')
        print(qq)
        qq = qq.replace(currency, '')
        num = float(qq)

    return num


num = 0

db = sqlite3.connect('Account.db')
cur = db.cursor()

cur.execute(f"SELECT COUNT(*) FROM Account")
h = int(cur.fetchone()[0])  # получаем кол-во записей в БД (на всякий случай обозначил тип)

x = h - (h - 1)
m = 0

SUM_LTC = 0
SUM_DOGE = 0
SUM_RUB = 0

while True:
    login(x)  # логинимся и далее действуем от этого логина
    time.sleep(0.1)
    LTC = balance(d.l, client)
    time.sleep(0.5)
    DOGE = balance(d.d, client)
    RUB = (LTC * d.coin['l'][d.t]) + (DOGE * d.coin['d'][d.t])
    print(str(RUB) + " RUB\n")

    SUM_LTC = SUM_LTC + LTC
    SUM_DOGE = SUM_DOGE + DOGE
    SUM_RUB = SUM_RUB + (SUM_LTC * d.coin['l'][d.t]) + (SUM_DOGE * d.coin['d'][d.t])

    if x == h:  # выходим из цикла, когда все аккаунты опрошены
        break
    time.sleep(0.5)
    x = x + 1

time.sleep(0.1)
print("Всего на всех аккаунтах при нынешнем курсе (" + str(d.coin['l'][d.t]) + ' RUB за 1 ' + d.coin['l'][d.name] + ', ' + str(d.coin['d'][d.t]) + ' RUB за 1 ' + d.coin['d'][d.name] + ") имеется:\n" + str(round(SUM_RUB, 2)) + " Рублей")

# while(True):
#     if x == h + 1:
#         print("Всего примерно добыто:")
#         print("LTC:    " + str(m) + "\nРублей: " + str(m * 12745.16))
#         break
#     cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
#     time.sleep(0.1)
#     Phone = str(cur.fetchone()[0])
#     print("Входим в аккаунт: " + Phone)
#     cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
#     time.sleep(0.1)
#     api_id = str(cur.fetchone()[0])
#     cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
#     time.sleep(0.1)
#     api_hash = str(cur.fetchone()[0])
#     session = str("anon" + str(x))
#     client = TelegramClient(session, api_id, api_hash)
#     client.start()
#
#     dlgs = client.get_dialogs()
#     for dlg in dlgs:
#         if dlg.title == COIN_name:
#             tegmo = dlg
#
#     client.send_message(COIN_name, "/balance")
#     time.sleep(1)
#     msgs = client.get_messages(tegmo, limit=1)
#
#     if COIN_name == LTC_bot:
#         currency = ' LTC'
#     else:
#         currency = ' DOGE'
#
#     for mes in msgs:
#         str_a = str(mes.message)
#         zz = str_a.replace('Available balance: ', '')
#         qq = zz.replace(currency, '')
#         print(qq)
#         waiting = float(qq)

# m = m + waiting
# print(m)
# x = x + 1
# time.sleep(1)
