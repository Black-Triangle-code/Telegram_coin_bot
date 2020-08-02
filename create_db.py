import sqlite3

conn = sqlite3.connect('accounts.db')
cur = conn.cursor()
# Создаем таблицу
cur.execute("""CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    phone TEXT UNIQUE,
    password TEXT,
    api_id TEXT,
    api_hash TEXT,
    activity BOOLEAN,
    litecoin_wallet TEXT
)""")

conn.commit()


def add_account():
    phone = input("Введите номер телефона: ")
    password = input("Введите пароль: ")
    api_id = input("Введите api_id: ")
    api_hash = input("Введите api_hash: ")
    activity = True if input("Аккаунт активен? [y/N] ").lower() == "y" else False
    litecoin_wallet = input("Введите LTC кошелёк: ")

    if input("Данные введены верно? [Y/n] ").lower() == "n":
        return
    cur.execute(
        "INSERT OR REPLACE INTO accounts(phone, password, api_id, api_hash, activity, litecoin_wallet) "
        "VALUES (?,?,?,?,?,?);",
        (phone, password, api_id, api_hash, activity, litecoin_wallet))
    conn.commit()


def remove_account():
    phone = input("Введите номер телефона: ")
    cur.execute("DELETE FROM accounts WHERE PHONE = ?", (phone,))
    conn.commit()


def list_accounts():
    cur.execute("SELECT phone, password, api_id, api_hash, activity, litecoin_wallet FROM accounts")
    accounts = cur.fetchall()
    accounts.insert(0, ["phone", "password", "api_id", "api_hash", "activity", "litecoin wallet"])
    max_lengths = [0] * len(accounts[0])
    for account in accounts:
        for i, e in enumerate(account):
            max_lengths[i] = max(max_lengths[i], len(str(e)))

    print(f"|{'|'.join(['-' * i for i in max_lengths])}|")
    for account in accounts:
        print(f"|{'|'.join([str(e).center(max_lengths[i]) for i, e in enumerate(account)])}|")
        print(f"|{'|'.join(['-' * i for i in max_lengths])}|")


def exit_program():
    cur.close()
    conn.close()
    exit(0)


actions = {
    1: add_account,
    2: remove_account,
    3: list_accounts,
    4: exit_program
}

while 1:
    action = input(f"1) Добавить аккаунт\n"
                   f"2) Удалить аккаунт\n"
                   f"3) Посмотреть аккаунты\n"
                   f"4) Выход\n")

    try:
        action = int(action)
        if action not in range(1, 4 + 1):
            raise ValueError("action not in range 1..4")
    except ValueError:
        print("Неверный ввод. Попробуйте ещё раз")
        continue

    actions[action]()
