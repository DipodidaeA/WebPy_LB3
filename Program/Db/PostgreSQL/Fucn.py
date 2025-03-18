from Db.PostgreSQL.Db import get_conn
from DTO.DTO import DTO

# отримання дня за id у PostgreSQL
def get_day_by_id_pg(id: int):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT d.id, d.dateID, d.temperatureID, dt.name, dt.dd, dt.mm, dt.yyyy, t.morning, t.noon, t.night "
        "FROM days d "
        "JOIN dates dt ON d.dateID = dt.id "
        "JOIN temperatures t ON d.temperatureID = t.id "
        "WHERE d.id = %s", (id,)
    )

    corteg = cursor.fetchone()

    if corteg is None:
        cursor.close()
        conn.close()
        return None

    cursor.close()
    conn.close()

    day = {
            "id": corteg[0],
            "dateID": corteg[1],
            "temperatureID": corteg[2],
            "date": {
                "name": corteg[3],
                "dd": corteg[4],
                "mm": corteg[5],
                "yyyy": corteg[6],
                "id": corteg[1]
            },
            "temperature": {
                "morning": corteg[7],
                "noon": corteg[8],
                "night": corteg[9],
                "id": corteg[2]
            }
        }

    return day

# отримання всіх днів у PostgreSQL
def get_all_days_pg():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT d.id, d.dateID, d.temperatureID, dt.name, dt.dd, dt.mm, dt.yyyy, t.morning, t.noon, t.night "
        "FROM days d "
        "JOIN dates dt ON d.dateID = dt.id "
        "JOIN temperatures t ON d.temperatureID = t.id "
    )

    corteg = cursor.fetchall()

    cursor.close()
    conn.close()

    days = [
        {
            "id": day[0],
            "dateID": day[1],
            "temperatureID": day[2],
            "date": {
                "name": day[3],
                "dd": day[4],
                "mm": day[5],
                "yyyy": day[6],
                "id": day[1]
            },
            "temperature": {
                "morning": day[7],
                "noon": day[8],
                "night": day[9],
                "id": day[2]
            }
        }
        for day in corteg
    ]

    return days

# створення дня у PostgreSQL
def add_day_pg(dto: DTO):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO dates (name, dd, mm, yyyy) VALUES (%s, %s, %s, %s) RETURNING id", 
        (dto.name, dto.dd, dto.mm, dto.yyyy)
    )
    new_date_id = cursor.fetchone()[0]
    
    cursor.execute(
        "INSERT INTO temperatures (morning, noon, night) VALUES (%s, %s, %s) RETURNING id", 
        (dto.morning, dto.noon, dto.night)
    )
    new_temp_id = cursor.fetchone()[0]
    
    cursor.execute(
        "INSERT INTO days (dateID, temperatureID) VALUES (%s, %s) RETURNING id", 
        (new_date_id, new_temp_id)
    )
    new_day_id = cursor.fetchone()[0]
    
    conn.commit()

    cursor.close()
    conn.close()

    return get_day_by_id_pg(new_day_id)

# оновлення дня у PostgreSQL
def update_day_pg(dto: DTO):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT dateID, temperatureID FROM days WHERE id = %s", (dto.id,))
    day = cursor.fetchone()

    if day is None:
        cursor.close()
        conn.close()
        return None

    date_id, temp_id = day

    cursor.execute(
        "UPDATE dates SET name = %s, dd = %s, mm = %s, yyyy = %s WHERE id = %s",
        (dto.name, dto.dd, dto.mm, dto.yyyy, date_id)
    )
    cursor.execute(
        "UPDATE temperatures SET morning = %s, noon = %s, night = %s WHERE id = %s",
        (dto.morning, dto.noon, dto.night, temp_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return get_day_by_id_pg(dto.id)

# видалення дня за id у PostgreSQL
def delete_day_pg(id: int):
    conn = get_conn()
    cursor = conn.cursor()

    day = get_day_by_id_pg(id)

    if day is None:
        cursor.close()
        conn.close()
        return None


    cursor.execute("DELETE FROM days WHERE id = %s", (id,))
    cursor.execute("DELETE FROM dates WHERE id = %s", (id,))
    cursor.execute("DELETE FROM temperatures WHERE id = %s", (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return day