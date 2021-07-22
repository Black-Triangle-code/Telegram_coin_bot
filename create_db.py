import os
import sqlite3

from dotenv import load_dotenv

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

load_dotenv()
Phone = os.getenv("PHONE")
password = os.getenv("PASSWORD")
Api_id = os.getenv("API_ID")
Api_hash = os.getenv("API_HASH")
Activity = os.getenv("ACTIVITY")
Litecoin = os.getenv("LITECOIN")

cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{Phone}'")
if cur.fetchone() is None:
    cur.execute(
        """INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY, LITECOIN) VALUES (?,?,?,?,?,?);""",
        (Phone, password, Api_id, Api_hash, Activity, Litecoin),
    )
    db.commit()
    print("Зарегистрирован:")
    for value in cur.execute("SELECT * FROM Account"):
        print(value)
