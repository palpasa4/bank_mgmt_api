from fastapi import APIRouter, Depends, HTTPException
from database.tables import UserSchema
from models.request_models import Login, User, Amount
from core.handlers.response_handler import json_response
from core.auth.auth_handler import sign_jwt
from core.auth.helpers import check_password, check_role
from core.auth.auth_bearer import JWTBearer
from core.handlers.logger_config import logger
from database.conn import db_dependency
from database.users_db import deposit, withdraw

router = APIRouter()


# user login
@router.post("/user/login")
async def user_login(user: Login, db: db_dependency):
    db_user = db.query(UserSchema).filter_by(username=user.username).first()
    if db_user is None or not check_password(user.password, str(db_user.password)):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return sign_jwt(str(db_user.cust_id))


# user: deposit
@router.post("/user/deposit", tags=["user_deposit"])
def deposit_amount(
    a: Amount, db: db_dependency, user_id: str = Depends(JWTBearer())
):  # use of depends?
    if check_role(user_id, db) != "user":
        raise HTTPException(status_code=403, detail="User not allowed!")
    if a.amount < 500:
        raise HTTPException(status_code=400, detail="Minimum amount of deposit is 500!")
    return deposit(a, user_id, db)


# user: withdraw
@router.post("/user/withdraw")
def withdraw_amount(a: Amount, db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) != "user":
        raise HTTPException(status_code=403, detail="User not allowed!")
    if a.amount < 500:
        raise HTTPException(
            status_code=400, detail="Minimum amount of withdrawal is 500!"
        )
    return withdraw(a, user_id, db)
