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

class RunChromeTests():
    def testMethod(self):
        selenium_url = "http://localhost:4444/wd/hub"
        caps = {'browserName': 'chrome'}
        driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps)
        driver.maximize_window()
        driver.get(url_rec)
        time.sleep(waitin + 10)
        driver.close()
        driver.quit()

db = sqlite3.connect('Account.db')
cur = db.cursor()

x = 1

while(True):
    n = 0
    u = 0
    print("Очередь аккаунта № " + str(x))
    if x == 23:
        x = x - 22
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
    client.send_message('LTC Click Bot', "🖥 Visit sites")
    time.sleep(30)
    while True:
        time.sleep(6)
        print("Нет заданий уже: " + str(u) + " раз")
        if u == 2:
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
                print ("Ждать придется: ", waitin)
                client.send_message('LTC Click Bot', "/visit")
                time.sleep(3)
                msgs2 = client.get_messages(tegmo, limit=1)
                for mes2 in msgs2:
                    button_data = mes2.reply_markup.rows[1].buttons[1].data
                    message_id = mes2.id
                    print("Перехожу по ссылке")
                    time.sleep(2)
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    ch = RunChromeTests()
                    ch.testMethod()
                    time.sleep(6)
                    fp = urllib.request.urlopen(url_rec)
                    mybytes = fp.read()
                    mystr = mybytes.decode("utf8")
                    fp.close()
                    if re.search(r'\bSwitch to reCAPTCHA\b', mystr):
                        from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                        resp = client(GetBotCallbackAnswerRequest(
                            'LTC Click Bot',
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
                messages = client.get_messages('Litecoin_click_bot')
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
                    print("Новая запись в файле сделана")
                    time.sleep(16)
                    n = n + 1

                    if n == 10:
                        break
    time.sleep(1)
    x = x + 1
    if x == 23:
        break
