from sqlalchemy.orm import joinedload, Session
from Db.SQLAlchemy.Models import Day, Date, Temperature
from DTO.DTO import DTO
from Db.SQLAlchemy.Db import SessionLocal

db = SessionLocal()

# отримання дня за id
def get_day_by_id(id: int):
    day = db.query(Day).filter_by(id=id).options(joinedload(Day.date), joinedload(Day.temperature)).first()

    return day

# отримання всіх днів
def get_all_days():
    days = db.query(Day).options(joinedload(Day.date), joinedload(Day.temperature)).all()

    return days

# додавання дня
def add_day(dto: DTO):
    new_date = Date(name=dto.name, dd=dto.dd, mm=dto.mm, yyyy=dto.yyyy)
    new_temperature = Temperature(morning=dto.morning, noon=dto.noon, night=dto.night)

    db.add(new_date)
    db.add(new_temperature)
    db.commit()
    db.refresh(new_date)
    db.refresh(new_temperature)

    new_day = Day(dateID=new_date.id, temperatureID=new_temperature.id)
    db.add(new_day)
    db.commit()
    db.refresh(new_day)

    return get_day_by_id(new_day.id)

# оновлення дня
def update_day(dto: DTO):
    day = db.query(Day).filter_by(id=dto.id).options(joinedload(Day.date), joinedload(Day.temperature)).first()

    if day == None:
        return None

    day.date.name = dto.name
    day.date.dd = dto.dd
    day.date.mm = dto.mm
    day.date.yyyy = dto.yyyy

    day.temperature.morning = dto.morning
    day.temperature.noon = dto.noon
    day.temperature.night = dto.night

    db.commit()
    db.refresh(day.date)
    db.refresh(day.temperature)
    db.refresh(day)

    return get_day_by_id(day.id)


# видалення дня
def delete_day(id: int):
    day = db.query(Day).filter_by(id=id).first()

    if day == None:
        return None
    
    date = db.query(Date).filter_by(id=day.dateID).first()
    temperature = db.query(Temperature).filter_by(id=day.temperatureID).first()

    db.delete(day)
    db.delete(date)
    db.delete(temperature)
    db.commit()

    return day