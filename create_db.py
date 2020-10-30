import sqlite3

db = sqlite3.connect('Account.db')
cur = db.cursor()
    # Создаем таблицу
cur.execute("""CREATE TABLE IF NOT EXISTS Account (
    ID INTEGER PRIMARY KEY,
    PHONE TEXT,
    PASS TEXT,
    API_ID TEXT,
    API_HASH TEXT,
    ACTIVITY TEXT,
    LTC TEXT,
    DOGE TEXT,
    BCH TEXT,
    BTC TEXT,
    ZEC TEXT
    
)""")

db.commit()

Phone = "0"
password = "1"
Api_id = "2"
Api_hash = "3"
Activity = "ON"
Ltc = "4"
Doge = "5"
Bch = "6"
Btc = "7"
Zec = "8"

cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{Phone}'")
if cur.fetchone() is None:
    cur.execute("""INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY, LTC, DOGE, BCH, BTC, ZEC) VALUES (?,?,?,?,?,?,?,?,?,?);""", (Phone, password, Api_id, Api_hash, Activity, Ltc, Doge, Bch, Btc, Zec))
    db.commit()
    print("Зарегистрированно!")
    for value in cur.execute("SELECT * FROM Account"):
        print(value)
