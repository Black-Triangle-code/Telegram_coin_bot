import re
import sqlite3
import time
import urllib.request

import requests

from selenium import webdriver

from telethon import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest


class RunChromeTests:
    def test_method(self):
        selenium_url = "http://localhost:4444/wd/hub"
        caps = {"browserName": "chrome"}
        driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps)
        driver.maximize_window()
        driver.get(url_rec)
        time.sleep(waitin + 10)
        driver.close()
        driver.quit()


db = sqlite3.connect("Account.db")
cur = db.cursor()

num = 1
while True:
    try:
        print("Очередь аккаунта № " + str(num))
        if num == 23:
            num = num - 22
        cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{num}'")
        time.sleep(0.4)
        Phone = str(cur.fetchone()[0])
        print("Входим в аккаунт: " + Phone)

        cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{num}'")
        time.sleep(0.4)
        api_id = str(cur.fetchone()[0])
        cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{num}'")
        time.sleep(0.4)
        api_hash = str(cur.fetchone()[0])
        session = str("anon" + str(num))
        client = TelegramClient(session, api_id, api_hash)
        client.start()
    except sqlite3.OperationalError:
        print("ERROR: Не найдены аккаунты")
        break

    dlgs = client.get_dialogs()
    for dlg in dlgs:
        if dlg.title == "LTC Click Bot":
            tegmo = dlg
    client.send_message("LTC Click Bot", "🖥 Visit sites")
    time.sleep(30)

    account = 0
    count = 0
    while True:
        time.sleep(6)
        print("Нет заданий уже: " + str(count) + " раз")
        if count == 2:
            print("Переходим на другой аккаунт")
            break
        print("Пройдено циклов: " + str(account))
        if account == 10:
            print("Переходим на другой аккаунт")
            break

        msgs = client.get_messages(tegmo, limit=1)
        for msg in msgs:
            if re.search(r"\bseconds to get your reward\b", msg.message):
                print("Найдено reward")
                str_a = str(msg.message)
                zz = str_a.replace("You must stay on the site for", "")
                qq = zz.replace("seconds to get your reward.", "")
                waitin = int(qq)
                print("Ждать придется: ", waitin)
                client.send_message("LTC Click Bot", "/visit")
                time.sleep(3)
                msgs2 = client.get_messages(tegmo, limit=1)
                for msg2 in msgs2:
                    button_data = msg2.reply_markup.rows[1].buttons[1].data
                    message_id = msg2.id
                    print("Перехожу по ссылке")
                    time.sleep(2)
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    ch = RunChromeTests()
                    ch.test_method()
                    time.sleep(6)
                    fp = urllib.request.urlopen(url_rec)
                    mybytes = fp.read()
                    mystr = mybytes.decode("utf8")
                    fp.close()
                    if re.search(r"\bSwitch to reCAPTCHA\b", mystr):
                        resp = client(GetBotCallbackAnswerRequest("LTC Click Bot", message_id, data=button_data))
                        time.sleep(2)
                        print("КАПЧА!")

                    else:
                        time.sleep(waitin)

                        time.sleep(2)
            elif re.search(r"\bSorry\b", msg.message):

                print("Найдено Sorry")
                count = count + 1
                print(count)

            else:
                messages = client.get_messages("Litecoin_click_bot")
                url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                my_file = open("per10.txt")
                fd = my_file.read()
                if fd == url_rec:
                    print("Найдено повторение переменной")
                    msgs2 = client.get_messages(tegmo, limit=1)
                    for msg2 in msgs2:
                        button_data = msg2.reply_markup.rows[1].buttons[1].data
                        message_id = msg2.id
                        resp = client(GetBotCallbackAnswerRequest(tegmo, message_id, data=button_data))
                        time.sleep(2)
                else:
                    waitin = 15
                    data1 = requests.get(url_rec).json
                    print(data1)

                    my_file = open("per10.txt", "w")
                    my_file.write(url_rec)
                    print("Новая запись в файле per10.txt сделана")
                    time.sleep(16)
                    account = account + 1

                    if account == 10:
                        break
    time.sleep(1)
    num = num + 1
    if num == 23:
        break
