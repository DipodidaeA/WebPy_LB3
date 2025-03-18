from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# створення базової моделі
Base = declarative_base()

# створення моделі Дня
class Day(Base):
    __tablename__ = 'Days'

    id = Column(Integer, primary_key=True, index=True)
    dateID = Column(Integer, ForeignKey('Dates.id'))
    temperatureID = Column(Integer, ForeignKey('Temperatures.id'))

    # зв'язки з моделями Date та Temperature
    date = relationship('Date')
    temperature = relationship('Temperature')

    
# створення моделі Інформація Про Дату
class Date(Base):
    __tablename__ = 'Dates'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dd = Column(Integer)
    mm = Column(Integer)
    yyyy = Column(Integer)


# створення моделі Інформація Про Температуру
class Temperature(Base):
    __tablename__ = 'Temperatures'

    id = Column(Integer, primary_key=True, index=True)
    morning = Column(Integer)
    noon = Column(Integer)
    night = Column(Integer)