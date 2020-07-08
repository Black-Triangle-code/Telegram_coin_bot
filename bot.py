import os
import time
import logging
import sqlite3

from bs4 import BeautifulSoup
import requests

from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.sync import TelegramClient
from config import *

requests.adapters.DEFAULT_RETRIES = 2
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

os.makedirs(URLS_FOLDER_PATH, exist_ok=True)


def skip_task(client, message, litecoin_bot):
    client(GetBotCallbackAnswerRequest(
        litecoin_bot,
        message.id,
        data=message.reply_markup.rows[1].buttons[1].data
    ))
    time.sleep(5)


with sqlite3.connect('accounts.db') as conn:
    cur = conn.cursor()

    cur.execute("SELECT id, phone, password, api_id, api_hash FROM accounts")
    accounts = cur.fetchall()

    cur.close()

for x, phone, password, api_id, api_hash in accounts:
    path_to_bad_urls = os.path.join(URLS_FOLDER_PATH, f"{x}.txt")
    no_tasks_count = 0  # Кол-во раз, когда не получилось найти заданий
    logging.info(f"Очередь аккаунта № {x}")
    logging.info(f"Входим в аккаунт: {phone}")
    client = TelegramClient(f"anon{x}", api_id, api_hash)
    client.start()

    litecoin_bot = client.get_entity("Litecoin_click_bot")
    messages = client.get_messages(litecoin_bot)
    if messages.total == 0:
        client.send_message(litecoin_bot, "/start")
        time.sleep(1)
    client.send_message(litecoin_bot, "/visit")

    if not os.path.exists(path_to_bad_urls):
        with open(path_to_bad_urls, "a+") as f:
            pass

    for loop_count in range(TASKS_COUNT):
        logging.info(f"Приступаем к {loop_count + 1} заданию из {TASKS_COUNT}")
        time.sleep(3)

        if no_tasks_count == TRIES_COUNT:
            logging.info("Заданий больше нет. Переходим на другой аккаунт")
            break

        message = client.get_messages(litecoin_bot)[0]

        if 'Sorry, there are no new ads available.' in message.message:
            no_tasks_count += 1
            logging.info("Похоже, что задания закончились. Попытка получить его ещё раз...")
            client.send_message(litecoin_bot, "/visit")
            time.sleep(10)
            continue

        url = message.reply_markup.rows[0].buttons[0].url
        with open(path_to_bad_urls, "r") as f:
            bad_urls = f.read().split('\n')

        if url in bad_urls:
            skip_task(client, message, litecoin_bot)
            continue
        try:
            soup = BeautifulSoup(requests.get(url).content, "lxml")
            time.sleep(2)  # Задержка из-за того, что бот не сразу присылает время, которое нужно ждать
        except requests.exceptions.ConnectionError as e:
            # Некоторые сайты, которые запрещены в РФ, почему-то не открываются. Может быть не доступен хост
            logging.error("Сайт недоступен")
            logging.exception(e, exc_info=True)
            client.send_message(litecoin_bot, "/visit")
            time.sleep(25)
            continue

        potential_captcha = soup.select_one('.card .card-body .text-center h6')

        if potential_captcha is not None and 'captcha' in potential_captcha.text.lower():
            logging.info('Найдена капча. Пропускаем задание...')
            skip_task(client, message, litecoin_bot)
            continue

        p = soup.select_one('#headbar.container-fluid')
        if p is not None:
            wait_time = int(p['data-timer'])
            logging.debug('+ request')
            logging.info(f"Ожидаем {wait_time} c.")
            time.sleep(wait_time + 1)
            r = requests.post('https://dogeclick.com/reward', data={'code': p['data-code'], 'token': p['data-token']})
            logging.debug(r.json())
        else:
            message = client.get_messages(litecoin_bot)[0]
            elements = list(filter(lambda i: i.isnumeric(), message.message.split(' ')))
            wait_time = int(elements[0]) if len(elements) == 1 else 25
            logging.info(f"Ожидаем {wait_time} c.")
            time.sleep(wait_time)
        message.mark_read()
        logging.info(f"Выполнено: {loop_count + 1} из {TASKS_COUNT}")

        with open(path_to_bad_urls, "a") as f:
            f.write(f"{url}\n")
