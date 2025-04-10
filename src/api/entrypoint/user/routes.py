from fastapi import APIRouter, Depends, HTTPException
from dbschemas.tables import UserSchema
from api.entrypoint.user.models import UserLoginModel, Amount
from core.auth.auth_handler import sign_jwt
from core.auth.helpers import check_password, check_role
from core.auth.auth_bearer import JWTBearer
from core.logconfig import logger
from src.api.dependencies import db_dependency
from modules.user.handlers import check_ifuser
from modules.user.handlers import (
    deposit,
    withdraw,
    user_view_details,
    user_view_transactions,\
    check_valid_user
)


router = APIRouter()


# user login
@router.post("/user/login",tags=["user_login"],status_code=200)
async def user_login(model: UserLoginModel, db: db_dependency):
    user = check_valid_user(model, db)
    token = sign_jwt(str(user.cust_id))
    logger.info(f"User login successful for username: {model.username}")
    return token


# user: deposit
@router.post("/user/deposit", tags=["user_deposit"],status_code=200)
def deposit_amount(
    model: Amount, db: db_dependency, id: str = Depends(JWTBearer())
):  
    check_ifuser(id,db)
    account=deposit(model,id,db)
    logger.info(f"Amount of {model.amount} deposited to bank account {account.bank_acc_id}")
    return {"message":f"Amount of {model.amount} successfully deposited to Bank Account {account.bank_acc_id}",
            "Deposited amount":model.amount,
            "Previous Balance":account.balance-model.amount,
            "New Balance":account.balance}


# user: withdraw
@router.post("/user/withdraw")
def withdraw_amount(
    model: Amount, db: db_dependency, id: str = Depends(JWTBearer())
):
    check_ifuser(id,db)
    account=withdraw(model,id,db)
    logger.info(f"Amount of {model.amount} withdrawn from bank account {account.bank_acc_id}")
    return {"message":f"Amount of {model.amount} successfully withdrawn from Bank Account {account.bank_acc_id}",
            "Deposited amount":model.amount,
            "Previous Balance":account.balance+model.amount,
            "New Balance":account.balance}


# view details
@router.get("/user/details")
def view_details(db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) != "user":
        raise HTTPException(status_code=403, detail="User not allowed!")
    return user_view_details(user_id, db)


# view transactions
@router.get("/user/transactions")
def view_transactions(db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) != "user":
        raise HTTPException(status_code=403, detail="User not allowed!")
    return user_view_transactions(user_id, db)
