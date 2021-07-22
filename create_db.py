import sqlite3

from config import activity, api_hash, api_id, litecoin, password, phone

db = sqlite3.connect("Account.db")
cur = db.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS Account (
    ID INTEGER PRIMARY KEY,
    PHONE TEXT,
    PASS TEXT,
    API_ID TEXT,
    API_HASH TEXT,
    ACTIVITY TEXT,
    LITECOIN TEXT
)"""
)
db.commit()

cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{phone}'")
if cur.fetchone() is None:
    cur.execute(
        """INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY, LITECOIN) VALUES (?,?,?,?,?,?);""",
        (phone, password, api_id, api_hash, activity, litecoin),
    )
    db.commit()
    print("Зарегистрирован:")
    for value in cur.execute("SELECT * FROM Account"):
        print(value)
