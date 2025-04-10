from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from decouple import config


DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT", cast=int)
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
