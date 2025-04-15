from fastapi import HTTPException
import time, jwt
from typing import Dict, Optional
from src.config.settings import  DefaultSettings






def token_response(token: str):
    return {"access_token": token}


def sign_jwt(user_id: str, settings: DefaultSettings) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(
        payload, 
        settings.secret.get_secret_value(), 
        algorithm=settings.algorithm,
    )
    return token_response(token)


# checks the validity of token: expiry time
def decode_jwt(token: str, settings:DefaultSettings) -> Optional[Dict[str, str]]:
    try:
        decoded_token = jwt.decode(token, settings.secret.get_secret_value(), algorithms=[settings.algorithm])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
