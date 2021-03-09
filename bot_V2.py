from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon import sync, events
import requests
import json
import hashlib
import time
import re
from telethon import TelegramClient
import webbrowser
import urllib.request
import os
import sqlite3
import threading
import dictionary as d



class RunChromeTests():
    def testMethod(self, url_rec, waitin):
        selenium_url = "http://localhost:4444/wd/hub"
        caps = {'browserName': 'chrome'}
        driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps)
        driver.maximize_window()
        driver.get(url_rec)
        time.sleep(waitin + 10)
        driver.close()
        driver.quit()


def login(x):
    if x == h + 1:
        x = h - (h - 1)
    print("Очередь аккаунта № " + str(x))
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


def bot(COIN_bot, CB):
    global x
    while True:
        n = 0
        u = 0
        # if x == h + 1:
        #     x = h - (h - 1)
        # print("Очередь аккаунта № " + str(x))

        # cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
        # time.sleep(0.1)
        # Phone = str(cur.fetchone()[0])
        # print("Входим в аккаунт: " + Phone)
        # cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
        # time.sleep(0.4)
        # api_id = str(cur.fetchone()[0])
        # cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
        # time.sleep(0.4)
        # api_hash = str(cur.fetchone()[0])
        # session = str("anon" + str(x))
        # client = TelegramClient(session, api_id, api_hash)
        # client.start()

        dlgs = client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == COIN_bot:
                tegmo = dlg
        client.send_message(COIN_bot, "🖥 Visit sites")
        time.sleep(30)
        while True:
            time.sleep(6)
            print("Нет заданий уже: " + str(u) + " раз")
            if u == 3:
                print("Переходим на другой аккаунт")
                break
            print("Пройдено циклов: " + str(n))
            if n == 10:
                print("Переходим на другой аккаунт")
                break
            msgs = client.get_messages(tegmo, limit=1)
            for mes in msgs:
                if re.search(r'\bseconds to get your reward\b', mes.message):
                    print("Найдено reward")
                    str_a = str(mes.message)
                    zz = str_a.replace('You must stay on the site for', '')
                    qq = zz.replace('seconds to get your reward.', '')
                    waitin = int(qq)
                    print("Ждать придется: ", waitin)
                    client.send_message(COIN_bot, "/visit")
                    time.sleep(3)
                    msgs2 = client.get_messages(tegmo, limit=1)
                    for mes2 in msgs2:
                        button_data = mes2.reply_markup.rows[1].buttons[1].data
                        message_id = mes2.id
                        print("Перехожу по ссылке")
                        time.sleep(2)
                        url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                        ch = RunChromeTests()
                        ch.testMethod(url_rec, waitin)
                        time.sleep(6)
                        fp = urllib.request.urlopen(url_rec)
                        mybytes = fp.read()
                        mystr = mybytes.decode("utf8")
                        fp.close()
                        if re.search(r'\bSwitch to reCAPTCHA\b', mystr):
                            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                            resp = client(GetBotCallbackAnswerRequest(
                                COIN_bot,
                                message_id,
                                data=button_data
                            ))
                            time.sleep(2)
                            print("КАПЧА!")

                        else:
                            time.sleep(waitin)

                            time.sleep(2)
                elif re.search(r'\bSorry\b', mes.message):

                    print("Найдено Sorry")
                    u = u + 1
                    print(u)

                else:
                    messages = client.get_messages(CB)
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    f = open("per10.txt")
                    fd = f.read()
                    if fd == url_rec:
                        print("Найдено повторение переменной")
                        msgs2 = client.get_messages(tegmo, limit=1)
                        for mes2 in msgs2:
                            button_data = mes2.reply_markup.rows[1].buttons[1].data
                            message_id = mes2.id
                            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                            resp = client(GetBotCallbackAnswerRequest(
                                tegmo,
                                message_id,
                                data=button_data
                            ))
                            time.sleep(2)
                    else:
                        waitin = 15
                        data1 = requests.get(url_rec).json
                        print(data1)

                        my_file = open('per10.txt', 'w')
                        my_file.write(url_rec)
                        print("Новая запись в 'per10.txt' сделана")
                        time.sleep(10)
                        n = n + 1

                        if n == 10:
                            break
        time.sleep(1)

        if x == h:
            print("КОНЕЧНЫЙ АККАУНТ")
            break
        x = x + 1


db = sqlite3.connect('Account.db')

cur = db.cursor()
cur.execute(f"SELECT COUNT(*) FROM Account")
time.sleep(0.1)


h = int(cur.fetchone()[0])
# LCB = 'Litecoin_click_bot'
# DCB = 'Dogecoin_click_bot'
# DOGE_bot = 'DOGE Click Bot'
# LTC_bot = 'LTC Click Bot'

# Lite = {'currency': ' LTC', 'bot': 'LTC Click Bot', 'cb': 'Litecoin_click_bot'}
# Doge = {'currency': ' DOGE', 'bot': 'DOGE Click Bot', 'cb': 'Dogecoin_click_bot'}
#
# coin = {'d': Doge, 'l': Lite}

x = h - (h - 1)

login(x)
bot(d.coin['l']['bot'], d.coin['l']['cb'])
bot(d.coin['d']['bot'], d.coin['d']['cb'])


# DOGE_thread = threading.Thread(target=bot, args=(coin['d']['bot'], coin['d']['cb']))
# LTC_thread = threading.Thread(target=bot, args=(coin['l']['bot'], coin['l']['cb']))
#
# DOGE_thread.start()
# LTC_thread.start()
#
# DOGE_thread.join()
# LTC_thread.join()
