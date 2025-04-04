import time, jwt, bcrypt
from database.tables import AdminSchema, UserSchema
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database.conn import get_db


# For successful login
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def check_role(user_id: str, db: Session = Depends(get_db)):
    valid_admin = db.query(AdminSchema).filter(AdminSchema.admin_id == user_id).first()
    valid_user = db.query(UserSchema).filter(UserSchema.cust_id == user_id).first()
    return "user" if not valid_admin else "admin"
