from sqlalchemy import create_engine
from Db.SQLAlchemy.Models import Base
from sqlalchemy.orm import sessionmaker

# шлях підключення до БД
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_wether_app.db'

# створення рушія БД
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# створення таблиць в БД
Base.metadata.create_all(engine)

# створення сесії для взаємодії з БД
SessionLocal = sessionmaker(autoflush=False ,bind=engine)