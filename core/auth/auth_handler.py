from fastapi import HTTPException
import time,jwt,bcrypt
from typing import Dict, Optional
from decouple import config
from database.tables import AdminSchema, UserSchema
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database.conn import get_db

#For successful login
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

#for generating JWT
JWT_SECRET = str(config("secret"))
JWT_ALGORITHM = str(config("algorithm"))

def token_response(token: str):
    return {
        "access_token": token
    }

def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

#checks the validity of token: expiry time
def decode_jwt(token: str)->Optional[Dict[str, str]]:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def check_role(user_id:str,db:Session=Depends(get_db)):
    valid_admin=db.query(AdminSchema).filter(AdminSchema.admin_id==user_id).first()
    valid_user=db.query(UserSchema).filter(UserSchema.cust_id==user_id).first()
    return "user" if not valid_admin else "admin"