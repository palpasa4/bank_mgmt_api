import time,jwt,bcrypt
from typing import Dict, Optional
from decouple import config

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
        "expires": time.time() + 120
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

# def validate_token(request:Request,db):
#     auth_header=request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer"):
#         raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
#     token=auth_header.split(" ")[1]
#     admin = db.query(models.AdminSchema).filter(models.AdminSchema.admin_id == token).first()
#     if admin:
#         return [token,"admin"]
#     user= db.query(models.UserSchema).filter(models.UserSchema.cust_id==token).first()
#     if user:
#         return [token,"user"]
#     raise HTTPException(status_code=401, detail="Unauthorized: Invalid token!")


# def validate_user_data(newuser:User)->None:
#     # data=load_json("database/user_data.json")
#     #Status code: 400 -> Bad Request -> Client side -> Input validation Errors
#     # if (any(user for user in data if user["username"] == newuser.username)):
#         raise HTTPException(status_code=400, detail="Username already exists!")
#     # if(len(newuser.username)<7):
#         raise HTTPException(status_code=400, detail="Username should contain atleast 7 characters!")
#     # if(newuser.opening_balance<500):
#         raise HTTPException(status_code=400, detail="Minimum opening balance is 500!")


# from datetime import timedelta, datetime
# from typing import Annotated
# from fastapi import APIRouter, Depends, HTTPException
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from starlette import status
# from database import SessionLocal
# from models import AdminSchema
# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from jose import jwt, JWTError
# import secrets

# router= APIRouter(
#     prefix='/auth',
#     tags=['auth']
# )
# # secret_key=secrets.token_hex(32)
# # print(secret_key)

# SECRET_KEY='0e525896b1a6fe9f129abc89413479123e6348c220dcea0f1a0ffec9d98a49b4'
# ALGORITHM ='HS256'

# bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
# oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')