import sqlite3


def get_all_accounts(filename='accounts.db'):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()

        cur.execute("SELECT id, phone, password, api_id, api_hash FROM accounts")
        accounts = cur.fetchall()

        cur.close()
    return accounts
