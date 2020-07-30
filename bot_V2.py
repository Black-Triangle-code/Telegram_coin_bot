# v2.1 (by v1a0)
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
import logging

logging.basicConfig(filename='coinbot1.log', filemode='a', format='%(asctime)s :: %(lineno)d :: %(message)s', level=logging.WARNING)
#logging.basicConfig(format='%(asctime)s :: %(lineno)d :: %(message)s', level=logging.WARNING)

# sqlite3.connect('Account.db') -> sqlite3.connect('Accounts.db')

log_phrases = {
    'get_accs_list':            'Getting accounts list from DB...',
    'acc_initialization':       'Initializing new account...',
    'mining':                   'Mining started...',
    'stat_upd_for_notify_bot':  'Updating status for notify_bot...',
    'get_main_dialog':          'Looking for a main dialog...',
    'start_message':            'Sending start message...',
    'get_last_msg_str':         'Getting last message as str...',
    'make_tasks':               'Starting tasks making...',
    'select_reactor':           'Selecting reactor...',
}


def autolog(func):
    phrase = log_phrases.get(f'{func.__name__}')
    if phrase is None:
        phrase = f'Function {func.__name__} in process...'

    def wrapper(*args, **kwargs):
        logging.warning(f'{phrase} ({func.__name__})')
        func(*args, **kwargs)
        logging.warning(f'Done. ({func.__name__})')

    return wrapper

def main():
    class controller:
        def __init__(self):
            self.accs_list = []
            self.done_counter = 0
            self.sorry_counter = 0
            self.main_dialog = False
            self.acc_id = ''
            self.phone = ''
            self.api_id = 0
            self.api_hash = ''
            self.session = ''
            self.main_dialog = False
            self.sleep_after_start = 20

        @autolog
        def get_accs_list(self):
            db = sqlite3.connect('Account.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Account")
            rows = cursor.fetchall()
            _list = []

            for row in rows:
                _list.append(
                    {
                        'id': row[0],
                        'phone': row[1],
                        'pass': row[2],
                        'api_id': row[3],
                        'api_hash': row[4],
                    }
                )

#            self.accs_list = _list[42:]
            self.accs_list = _list

        @autolog
        def acc_initialization(self, acc):
            self.done_counter = 0
            self.sorry_counter = 0
            self.main_dialog = False
            self.acc_id = acc.get('id')
            self.phone = acc.get('phone')
            self.api_id = acc.get('api_id')
            self.api_hash = acc.get('api_hash')
            self.session = f"anon{self.acc_id}"

        @autolog
        def stat_upd_for_notify_bot(self):
            status_file = open('queue.tmp', 'w')
            status_file.write(f"{self.acc_id}")
            status_file.close()

        def login_bot(self):
            logging.warning(f"\n\n\nLogging as: {self.phone} (bot {self.acc_id})\n")
            self.client = TelegramClient(self.session, self.api_id, self.api_hash)
            self.client.start()

        @autolog
        def get_main_dialog(self):
            # ?????????????????????????
            self.main_dialog = False
            for dialog in self.client.get_dialogs():
                if dialog.title == 'LTC Click Bot':
                    self.main_dialog = dialog

        @autolog
        def start_message(self):
            logging.warning("Time to sleep: {time_set}+2 ({realtime}) sec".format(
                time_set=self.sleep_after_start,
                realtime=self.sleep_after_start+2
            ))

            self.client.send_message('LTC Click Bot', "/menu")
            time.sleep(2)
            self.client.send_message('LTC Click Bot', "🖥 Visit sites")
            time.sleep(self.sleep_after_start)

        @autolog
        def get_last_msg_str(self):
            #self.last_msg_str = self.client.get_messages(self.main_dialog)[0].message
            time.sleep(3)
            self.last_msg_str = self.client.get_messages('Litecoin_click_bot', limit=2)[0].message
            logging.warning(f'Message is: \n{self.last_msg_str}')

        @autolog
        def get_previous_msg_str(self):
            try:
                time.sleep(3)
                self.previous_msg_str = self.client.get_messages('Litecoin_click_bot', limit=2)[1].message
                logging.warning(f'PRE-Message is: \n{self.previous_msg_str}')

            except Exception as e:
                logging.warning(e)
                self.previous_msg_str = ''

        @autolog
        def sorry_reactor(self):
            self.start_message()
            self.sorry_counter += 1

        @autolog
        def skip_task(self):
            self.client.send_message('LTC Click Bot', "/visit")
            time.sleep(3)
            msgs_2 = self.client.get_messages('Litecoin_click_bot')
            self.skip_message_id = msgs_2[0].id
            self.skip_button_data = msgs_2[0].reply_markup.rows[1].buttons[1].data

            from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
            self.client(GetBotCallbackAnswerRequest(
                'LTC Click Bot',
                self.skip_message_id,
                data=self.skip_button_data
            ))
            time.sleep(2)

        @autolog
        def get_time_to_wait(self):
            try:
                if re.search(r'seconds to get your reward', self.last_msg_str):
                    self.time_to_wait = int(re.search(r'\d+', self.last_msg_str).group())
                else:
                    self.time_to_wait = 4

            except Exception as e:
                self.time_to_wait = 30
                logging.warning(e)

        @autolog
        def calculate_profit(self):
            try:
                profit = 0
                with open('profit_', 'r') as profit_file:
                    for line in profit_file.readlines():
                        profit = float(line)

                new_money = float(re.search(r'\d+.\d+', self.previous_msg_str[:45]).group())
                new_profit = float(profit + new_money)

                logging.warning('\n'
                                f'money: {"{0:.8f}".format(new_money)}\n'
                                f'had__: {"{0:.8f}".format(profit)}\n'
                                f'itog_: {"{0:.8f}".format(new_profit)}\n')

                with open('profit_', 'w') as profit_file:
                    profit_file.write(f'{"{0:.8f}".format(new_profit)}')


                logging.warning(f'{"=" * 10}\nPROFIT: {"{0:.8f}".format(ltc_profit)} LTC')

            except Exception as e:
                logging.warning(e)

        @autolog
        def chrome_test(self):
            logging.warning(f'Time to wait: {self.time_to_wait}')
            selenium_url = "http://localhost:4444/wd/hub"
            caps = {'browserName': 'chrome'}
            driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps)
            driver.maximize_window()
            driver.get(self.adw_url)
            time.sleep(self.time_to_wait + 10 if self.time_to_wait > 4 else 4)
            driver.close()
            driver.quit()

        @autolog
        def chrome_reactor(self):
            self.client.send_message('LTC Click Bot', "/visit")
            time.sleep(3)

            try_counter = 0

            while try_counter < 2:
                try:
                    self.chrome_test()
                    break
                except Exception as e:
                    logging.warning(f'\n         Chrome crushed (1)')
                    logging.warning(e)
                    try_counter += 1


        @autolog
        def req_reactor(self):
            self.previous_msg_str = ''
            self.client.send_message('LTC Click Bot', "/visit")
            time.sleep(3)

            self.get_last_msg_str()
            msgs_2 = self.client.get_messages('Litecoin_click_bot', limit=2)
            self.adw_url = msgs_2[0].reply_markup.rows[0].buttons[0].url

            self.get_time_to_wait()
            self.chrome_reactor()

            logging.warning('\nWaiting for an answer...')

            self.get_last_msg_str()
            if re.search(r'stay on the site for at', self.last_msg_str):
                temp_req = requests.get(self.adw_url).json
                time.sleep(5)
                self.get_last_msg_str()

            if re.search(r'seconds to get your reward', self.last_msg_str):
                self.get_time_to_wait()
                self.chrome_reactor()

            self.get_previous_msg_str()
            if re.search(r'You earned', self.previous_msg_str):
                self.done_counter += 1
                self.calculate_profit()
                return logging.warning('Task done! Ez-pz!')

            if re.search(r'Sorry, there are no new ads available', self.last_msg_str):
                self.done_counter += 1
                return logging.warning('Task done! Ez-pz!')

            else:
                self.skip_task()
                return logging.warning('Task skipped')


        @autolog
        def select_reactor(self):
            self.get_last_msg_str()

            if re.search(r'Sorry, there are no new ads available.', self.last_msg_str):
                self.sorry_reactor()

            #elif re.search(r'\bseconds to get your reward\b', self.last_msg_str):
            #    self.chrome_reactor()

            else:
                self.req_reactor()

        @autolog
        def make_tasks(self):
            while True:
                logging.warning(f"Bot {self.acc_id} has DONE {self.done_counter} tasks")

                if self.sorry_counter == 2:
                    logging.warning("Have no ads 2 times")
                    logging.warning("Moving to the next account")
                    break

                elif self.done_counter == 16:
                    logging.warning("Moving to the next account")
                    break

                else:
                    self.select_reactor()

        @autolog
        def mining(self):
            self.get_accs_list()

            if self.accs_list:
                for acc in self.accs_list:
                    try:
                        self.acc_initialization(acc)
                        self.stat_upd_for_notify_bot()
                        self.login_bot()
                        self.get_main_dialog()
                        if not bool(self.main_dialog):
                            logging.warning(f'{self.phone} (bot {self.acc_id}) HAVE NO LITECOIN BOT!!!')
                            break

                        else:
                            self.start_message()
                            self.get_last_msg_str()

                            if self.last_msg_str is not "🖥 Visit sites":
                                self.make_tasks()

                            else:
                                logging.warning("Didn't get an answer for a start_message()")

                    except Exception as e:
                        logging.warning(f'\n\n WE ARE DOWN \nError: {e}')
                        pass

                time.sleep(3)
            else:
                logging.warning('No accounts list is empty')

    bots = controller()
    bots.mining()


if __name__ == '__main__':
    logging.warning('''
    #===================================#
    #===================================#
    #===================================#
    ''')
    main()