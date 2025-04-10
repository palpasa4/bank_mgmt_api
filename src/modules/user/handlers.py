from sqlalchemy import select
from dbschemas.tables import UserSchema, BankAccount, Transactions
from src.api.entrypoint.user.models import *
from src.api.entrypoint.user.responses import *
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.api.dependencies import get_db
from core.auth.helpers import hash_password, check_password, check_role
from core.logconfig import logger
from src.modules.user.queries import get_user, add_balance, deduct_balance
from src.modules.admin.exceptions import *
from src.core.handlers.exceptions import *
from src.modules.user.exceptions import *


def check_valid_user(model: UserLoginModel, db):
    user = get_user(model, db)
    if user is None or not check_password(
        model.password.get_secret_value(), str(user.password)
    ):
        logger.warning(
            f"Failed user login attempt: Username: {model.username} Password:{model.password}"
        )
        raise InvalidUserLoginException(
            message=f"Login Failed: Invalid username or password.", status_code=401
        )
    return user


def check_ifuser(id: str, db):
    if check_role(id, db) != "user":
        logger.error(f"Unauthorized access attempt by admin {id}")
        raise AdminPermissionDeniedException(
            message="User not allowed.", status_code=401
        )


def deposit(model: Amount, id: str, db):
    if model.amount < 500:
        logger.error(
            "DepositBalanceException: Trying to deposit less than minimum amount!"
        )
        raise DepositBalanceException(
            message="Minimum amount of deposit is 500!", status_code=400
        )
    try:
        account = add_balance(model, id, db)
        return account
    except Exception as e:
        logger.error(f"Database error: Unable to deposit amount for user with ID: {id}")
        raise DatabaseException(
            message="Database error: Unable to deposit money.", status_code=500
        )


def withdraw(model: Amount, id: str, db):
    bank_acc = db.query(BankAccount).filter(BankAccount.cust_id == id).first()
    if model.amount < 500:
        logger.error(
            "WithdrawBalanceException: Trying to withdraw less than minimum amount!"
        )
        raise DepositBalanceException(
            message="Minimum amount of withdrawal is 500!", status_code=400
        )
    if (
        bank_acc
        and isinstance(bank_acc.balance, (float))
        and float(bank_acc.balance) - 500 < model.amount
    ):
        logger.error(
            "WithdrawBalanceException: Trying to withdraw more than existing balance!"
        )
        raise WithdrawBalanceException(
            message=f"Withdrawal exceeds existing balance. Minimum existing balance should be NPR 500 Existing balance is : {bank_acc.balance}",
            status_code=400,
        )
    try:
        account = deduct_balance(model, id, db)
        return account
    except Exception as e:
        logger.error(
            f"Database error: Unable to withdraw amount for user with ID: {id}"
        )
        raise DatabaseException(
            message="Database error: Unable to withdraw money.", status_code=500
        )


# remaining work
def user_view_details(user_id: str, db: Session = Depends(get_db)):
    details = db.execute(
        select(
            UserSchema.cust_id,
            UserSchema.username,
            BankAccount.bank_acc_id,
            BankAccount.fullname,
            BankAccount.address,
            BankAccount.contact_no,
            BankAccount.balance,
            BankAccount.updated_at,
        )
        .outerjoin(BankAccount, UserSchema.cust_id == BankAccount.cust_id)
        .where(UserSchema.cust_id == user_id)
    ).fetchone()
    if not details:
        return {"error": "No data found."}
    return {"details": UserViewDetails(**dict(details._mapping))}


def user_view_transactions(user_id: str, db: Session = Depends(get_db)):
    bank_acc_id = db.execute(
        select(BankAccount.bank_acc_id).where(BankAccount.cust_id == user_id)
    ).scalar()
    transactions = db.execute(
        select(Transactions).where(Transactions.bank_acc_id == bank_acc_id)
    ).fetchall()
    if not transactions:
        return {"error": "No transactions found"}
    return {
        "transactions": [
            UserTransactionDetails(**transaction[0].__dict__)
            for transaction in transactions
        ]
    }
