from telethon.sync import TelegramClient
import utils
import config

accounts = utils.get_all_accounts()

for x, phone, password, api_id, api_hash in accounts:
    print(f"Очередь аккаунта № {x}\n"
          f"Входим в аккаунт: {phone}")
    session = f"{config.TELETHON_SESSION_NAME}{x}"
    client = TelegramClient(session, api_id, api_hash)
    client.start(phone, password=password)


print("Аккаунты активированы!")
