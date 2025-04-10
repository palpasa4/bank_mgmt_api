from fastapi import HTTPException
import time, jwt, bcrypt
from typing import Dict, Optional
from decouple import config
from dbschemas.tables import AdminSchema, UserSchema
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session


# for generating JWT
JWT_SECRET = str(config("secret"))
JWT_ALGORITHM = str(config("algorithm"))


def token_response(token: str):
    return {"access_token": token}


def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


# checks the validity of token: expiry time
def decode_jwt(token: str) -> Optional[Dict[str, str]]:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
