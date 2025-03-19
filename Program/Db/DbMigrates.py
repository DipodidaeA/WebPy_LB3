from Db.SQLAlchemy.Db import SessionLocal
from Db.SQLAlchemy.Models import Day, Date, Temperature
from Db.SQLAlchemy.Func import add_day
from Db.MongoDB.Db import dbmo
from DTO.DTO import DTO
from Db.MongoDB.Func import add_day_mo, get_all_days_mo

# міграція даних з SQLite у MongoDB
def mgrate_SQLite_on_MO():
   db = SessionLocal()

   collection_days = dbmo["days"]
   collection_dates = dbmo["dates"]
   collection_temps = dbmo["temperatures"]

   # отримуємо всі дані SQLite
   days = db.query(Day).all()
   dates = {d.id: d for d in db.query(Date).all()}
   temperatures = {t.id: t for t in db.query(Temperature).all()}

   # видаляємо всі дані у MongoDB
   collection_days.delete_many({})
   collection_dates.delete_many({})
   collection_temps.delete_many({})

   # записуємо дані з SQLite у MongoDB
   for day in days:
      date = dates.get(day.dateID)
      temp = temperatures.get(day.temperatureID)

      dto = DTO(
         id = "0",
         name = date.name,
         dd = date.dd,
         mm = date.mm,
         yyyy = date.yyyy,
         morning = temp.morning,
         noon = temp.noon,
         night = temp.night
      )

      add_day_mo(dto)

   return

# міграція даних з MongoDB у SQLite
def mgrate_MO_on_SQLite():
   db = SessionLocal()

   # отримуємо дані з MongoDb
   days = get_all_days_mo()

   # видаляємо дані з SQLite
   db.query(Date).delete()
   db.query(Temperature).delete()
   db.query(Day).delete()
   db.commit()

   # записуємо дані з MongoDB у SQLite
   for day in days:
      dto = DTO(
         id = "0",
         name = day["date"]["name"],
         dd = day["date"]["dd"],
         mm = day["date"]["mm"],
         yyyy = day["date"]["yyyy"],
         morning = day["temperature"]["morning"],
         noon = day["temperature"]["noon"],
         night = day["temperature"]["night"]
      )

      add_day(dto)

   return