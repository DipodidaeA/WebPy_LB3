import psycopg2

# стадія 3 підключення до БД
# після виконання скриптів створення БД та таблиць,
# можемо підключатися до БД та взаємодіяти з даними
def get_conn():
    conn = psycopg2.connect(
        dbname="sql_wether_app_pg",
        user="postgres",
        password="123",
        host="127.0.0.1",
        port="5432"
    )

    return conn

'''
стадія 2 сворення БД
скрипт для створення таблиць БД

conn = psycopg2.connect(
    dbname="sql_wether_app_pg",
    user="postgres",
    password="123",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Dates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dd INT NOT NULL,
    mm INT NOT NULL,
    yyyy INT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Temperatures (
    id SERIAL PRIMARY KEY,
    morning INT NOT NULL,
    noon INT NOT NULL,
    night INT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Days (
    id SERIAL PRIMARY KEY,
    dateID INT REFERENCES Dates(id) NOT NULL,
    temperatureID INT REFERENCES Temperatures(id) NOT NULL
)
""")

conn.commit()
cur.close()
conn.close()
'''

'''
стадія 1 створення БД
скрипт для створення БД

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123",
    host="127.0.0.1",
    port="5432"
)
conn.autocommit = True
cur = conn.cursor()

cur.execute("CREATE DATABASE sql_wether_app_pg;")

cur.close()
conn.close()
'''