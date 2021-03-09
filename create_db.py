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
    LITECOIN TEXT,
    DOGECOIN TEXT
)""")

db.commit()

print("API_ID и API_HASH можно получить на сайте - https://my.telegram.org/apps")
while True:
    Phone = str(input("Номер телефона включая +7**********:\n"))  # "+7**********"
    password = "12345NEon"
    Api_id = str(input("Введите API_ID:\n"))  # "3******6"
    Api_hash = str(input("Введите API_HASH\n"))  # "12*************************ea"
    Activity = "ON"
    Litecoin = str(input("Введите адрес кошелька Litecoin:\n"))  # "ltc1***************************************a8el"
    Dogecoin = str(input("Введите адрес кошелька Dogecoin:\n"))  # "DADWGC********************3K4ZrEtrZ"
    while True:
        check = input("\nВсё верно?\nНомер: " + Phone + "\nApi_id: " + Api_id + "\nApi_hash: " + Api_hash + "\nКошельки: " + Litecoin + "   " + Dogecoin +
        "\nЕсли необходимо что-то изменить, введите 'phone', 'id', 'hash', 'D', или 'L' без ковычек, иначе просто нажмите Enter...\n")
        check = check.lower()
        if check == 'phone':
            Phone = str(input())
            continue
        elif check == 'id':
            Api_id = str(input())
            continue
        elif check == 'hash':
            Api_hash = str(input())
            continue
        elif check == 'l':
            Litecoin = str(input())
            continue
        elif check == 'd':
            Dogecoin = str(input())
            continue
        else:
            break
    break

cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{Phone}'")
if cur.fetchone() is None:
    cur.execute("""INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY, LITECOIN, DOGECOIN) VALUES (?,?,?,?,?,?,?);""", (Phone, password, Api_id, Api_hash, Activity, Litecoin, Dogecoin))
    db.commit()
    print("Зарегистрированно!")
    for value in cur.execute("SELECT * FROM Account"):
        print(value)
