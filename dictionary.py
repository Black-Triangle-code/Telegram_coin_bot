import requests
from bs4 import BeautifulSoup
import time

URL_LTC = 'https://pokur.su/ltc/rub/1/'
URL_DOGE = 'https://pokur.su/doge/rub/1/'


def park(url):
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    inRUB = soup.findAll("span", {"class": "pretty-sum"})
    factor = inRUB[1].text
    factor = factor.replace(',', '.')
    factor = float(factor)
    time.sleep(0.5)
    return factor


doge = park(URL_DOGE)
ltc = park(URL_LTC)

Lite = {'name': 'LTC', 'currency': ' LTC', 'bot': 'LTC Click Bot', 'cb': 'Litecoin_click_bot', 'l_minimum_withdraw': 0.0003, 'transfer': ltc}
Doge = {'name': 'DOGE', 'currency': ' DOGE', 'bot': 'DOGE Click Bot', 'cb': 'Dogecoin_click_bot', 'l_minimum_withdraw': 2, 'transfer': doge}

coin = {'d': Doge, 'l': Lite}

name = 'name'
currency = 'currency'
bot = 'bot'
cb = 'cb'
t = 'transfer'
l_minimum = 'l_minimum_withdraw'
