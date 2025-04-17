from src.api.entrypoint.user.responses import UserViewDetails
from fastapi import APIRouter, Depends, HTTPException
from src.dbschemas.user import UserSchema
from src.api.entrypoint.user.models import UserLoginModel, Amount
from src.core.auth.auth_handler import sign_jwt
from src.core.auth.helpers import check_password, check_role
from src.core.auth.auth_bearer import JWTBearer
from src.core.logconfig import logger
from src.api.dependencies import AnnotatedDatabaseSession, AnnotatedDefaultSettings
from src.modules.user.handlers import check_ifuser
from src.api.entrypoint.user.responses import UserTransactionDetails
from src.config.settings import DefaultSettings
from src.modules.user.handlers import (
    deposit,
    withdraw,
    user_view_details,
    user_view_transactions,
    check_valid_user,
)


router = APIRouter(prefix="/user", tags=["user"])


# user login
@router.post("/login/", tags=["user_login"], status_code=200)
async def user_login(
    model: UserLoginModel,
    settings: AnnotatedDefaultSettings,
    db: AnnotatedDatabaseSession,
):
    user = check_valid_user(model, db)
    token = sign_jwt(str(user.cust_id), settings)
    logger.info(f"User login successful for username: {model.username}")
    return token


# user: deposit
@router.post("/deposit/", tags=["user_deposit"], status_code=200)
def deposit_amount(
    model: Amount, db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())
):
    check_ifuser(id, db)
    account = deposit(model, id, db)
    logger.info(
        f"Amount of {model.amount} deposited to bank account {account.bank_acc_id}"
    )
    return {
        "message": f"Amount of {model.amount} successfully deposited to Bank Account {account.bank_acc_id}",
        "Deposited amount": model.amount,
        "Previous Balance": account.balance - model.amount,
        "New Balance": account.balance,
    }


# user: withdraw
@router.post("/withdraw/")
def withdraw_amount(
    model: Amount, db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())
):
    check_ifuser(id, db)
    account = withdraw(model, id, db)
    logger.info(
        f"Amount of {model.amount} withdrawn from bank account {account.bank_acc_id}"
    )
    return {
        "message": f"Amount of {model.amount} successfully withdrawn from Bank Account {account.bank_acc_id}",
        "Deposited amount": model.amount,
        "Previous Balance": account.balance + model.amount,
        "New Balance": account.balance,
    }


# view details
@router.get("/details/")
def view_details(db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())):
    check_ifuser(id, db)
    details = user_view_details(id, db)
    return {"details": UserViewDetails(**dict(details._mapping))}


# view transactions
@router.get("/transactions/")
def view_transactions(db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())):
    check_ifuser(id, db)
    transactions = user_view_transactions(id, db)
    return {
        "transactions": [
            UserTransactionDetails(**transaction[0].__dict__)
            for transaction in transactions
        ]
    }
