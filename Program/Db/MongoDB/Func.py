from Db.MongoDB.Db import dbmo
from DTO.DTO import DTO
from bson import ObjectId

collection_days = dbmo["days"]
collection_dates = dbmo["dates"]
collection_temps = dbmo["temperatures"]

def get_day_by_id_mo(id: str):
    day = collection_days.find_one({"_id": ObjectId(id)})
    date = collection_dates.find_one({"_id": ObjectId(day["dateID"])})
    temperature = collection_temps.find_one({"_id": ObjectId(day["temperatureID"])})

    day_ = {
            "id": str(day["_id"]),
            "dateID": str(date["_id"]),
            "temperatureID": str(temperature["_id"]),
            "date": {
                "id": str(date["_id"]),
                "name": date["name"],
                "dd": date["dd"],
                "mm": date["mm"],
                "yyyy": date["yyyy"]
            },
            "temperature": {
                "id": str(temperature["_id"]),
                "morning": temperature["morning"],
                "noon": temperature["noon"],
                "night": temperature["night"]
            }
        }

    return day_

def get_all_days_mo():
    days_list = collection_days.find()
    days = []

    for day in days_list:
        date = collection_dates.find_one({"_id": ObjectId(day["dateID"])})
        temperature = collection_temps.find_one({"_id": ObjectId(day["temperatureID"])})

        days.append({
            "id": str(day["_id"]),
            "dateID": str(date["_id"]),
            "temperatureID": str(temperature["_id"]),
            "date": {
                "id": str(date["_id"]),
                "name": date["name"],
                "dd": date["dd"],
                "mm": date["mm"],
                "yyyy": date["yyyy"]
            },
            "temperature": {
                "id": str(temperature["_id"]),
                "morning": temperature["morning"],
                "noon": temperature["noon"],
                "night": temperature["night"]
            }
        })

    return days

def add_day_mo(dto):
    new_date = {
        "name": dto.name,
        "dd": dto.dd,
        "mm": dto.mm,
        "yyyy": dto.yyyy
    }
    date_inserted = collection_dates.insert_one(new_date)
    date_id = date_inserted.inserted_id

    new_temperature = {
        "morning": dto.morning,
        "noon": dto.noon,
        "night": dto.night
    }
    temp_inserted = collection_temps.insert_one(new_temperature)
    temperature_id = temp_inserted.inserted_id

    new_day = {
        "dateID": str(date_id),
        "temperatureID": str(temperature_id)
    }
    day_inserted = collection_days.insert_one(new_day)
    day_id = day_inserted.inserted_id

    return get_day_by_id_mo(str(day_id))

def update_day_mo(dto: DTO):
    day = collection_days.find_one({"_id": ObjectId(dto.id)})

    if day is None:
        return None

    collection_dates.update_one(
        {"_id": ObjectId(day["dateID"])},
        {"$set": {
            "name": dto.name,
            "dd": dto.dd,
            "mm": dto.mm,
            "yyyy": dto.yyyy
        }}
    )

    collection_temps.update_one(
        {"_id": ObjectId(day["temperatureID"])},
        {"$set": {
            "morning": dto.morning,
            "noon": dto.noon,
            "night": dto.night
        }}
    )

    return get_day_by_id_mo(dto.id)

def delete_day_mo(id: str):
    day = get_day_by_id_mo(id)

    if day is None:
        return None

    date_id = day["dateID"]
    temperature_id = day["temperatureID"]

    collection_days.delete_one({"_id": ObjectId(id)})
    collection_dates.delete_one({"_id": ObjectId(date_id)})
    collection_temps.delete_one({"_id": ObjectId(temperature_id)})

    return day