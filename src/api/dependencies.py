from src.core.extensions.conn import Base, SessionLocal, sessionmaker, Session, engine
from typing import Annotated
from fastapi import Depends


def init_db():
    Base.metadata.create_all(bind=engine)


# connection to db: dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
