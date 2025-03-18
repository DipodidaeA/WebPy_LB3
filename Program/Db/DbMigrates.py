from Db.SQLAlchemy.Db import SessionLocal
from Db.SQLAlchemy.Models import Day, Date, Temperature
from Db.PostgreSQL.Db import get_conn

# міграція даних з SQLite у PostgreSQL
def mgrate_SQLite_on_PG():
    db = SessionLocal()
    conn = get_conn()
    cursor = conn.cursor()

    # отримуємо всі дані SQLite
    days = db.query(Day).all()
    dates = {d.id: d for d in db.query(Date).all()}
    temperatures = {t.id: t for t in db.query(Temperature).all()}

    # видаляємо всі дані у PostgreSQL
    cursor.execute("DELETE FROM days")
    cursor.execute("DELETE FROM temperatures")
    cursor.execute("DELETE FROM dates")
    conn.commit()

    # записуємо дані з SQLite у PostgreSQL
    for day in days:
        date = dates.get(day.dateID)
        temp = temperatures.get(day.temperatureID)

        if date and temp:
            cursor.execute(
                "INSERT INTO dates (id, name, dd, mm, yyyy) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                (date.id, date.name, date.dd, date.mm, date.yyyy)
            )

            cursor.execute(
                "INSERT INTO temperatures (id, morning, noon, night) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                (temp.id, temp.morning, temp.noon, temp.night)
            )

            cursor.execute(
                "INSERT INTO days (id, dateID, temperatureID) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING",
                (day.id, day.dateID, day.temperatureID)
            )

    conn.commit()

    cursor.close()
    conn.close()

    return

# міграція даних з PostgreSQL у SQLite
def mgrate_PG_on_SQLite():
    db = SessionLocal()
    conn = get_conn()
    cursor = conn.cursor()

    # отримуємо дані з PostgreSQL
    cursor.execute("SELECT id, name, dd, mm, yyyy FROM dates")
    dates = cursor.fetchall()

    cursor.execute("SELECT id, morning, noon, night FROM temperatures")
    temperatures = cursor.fetchall()

    cursor.execute("SELECT id, dateID, temperatureID FROM days")
    days = cursor.fetchall()

    # видаляємо дані з SQLite
    db.query(Date).delete()
    db.query(Temperature).delete()
    db.query(Day).delete()
    db.commit()

    # записуємо дані з PostgreSQL у SQLite
    for date in dates:
        db.add(Date(id=date[0], name=date[1], dd=date[2], mm=date[3], yyyy=date[4]))

    for temp in temperatures:
        db.add(Temperature(id=temp[0], morning=temp[1], noon=temp[2], night=temp[3]))

    for day in days:
        db.add(Day(id=day[0], dateID=day[1], temperatureID=day[2]))

    db.commit()

    return