import uuid, hashlib
from datetime import datetime
from sqlalchemy import desc, select
from dbschemas.tables import UserSchema, BankAccount, Transactions
from core.auth.helpers import hash_password
from api.entrypoint.user.models import Login, Amount
from src.api.entrypoint.admin.models import CreateUserModel
from api.entrypoint.user.responses import UserViewDetails, UserTransactionDetails
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.api.dependencies import get_db
from returns.result import safe, Success, Failure
from core.handlers.exceptions import DuplicateResourceException


def deposit(a: Amount, user_id: str, db: Session = Depends(get_db)):
    db.query(BankAccount).filter(BankAccount.cust_id == user_id).update(
        {
            BankAccount.balance: BankAccount.balance + a.amount,
            BankAccount.updated_at: datetime.now(),
        }
    )
    db.commit()
    return {"message": f"Deposited a balance of {a.amount}"}


def withdraw(a: Amount, user_id: str, db: Session = Depends(get_db)):
    bank_acc = db.query(BankAccount).filter(BankAccount.cust_id == user_id).first()
    if (
        bank_acc
        and isinstance(bank_acc.balance, (float))
        and float(bank_acc.balance) - 500 < a.amount
    ):
        raise HTTPException(
            status_code=400,
            detail=f"No sufficient amount for withdrawal. Minimum existing balance should be NPR 500.",
        )
    db.query(BankAccount).filter(BankAccount.cust_id == user_id).update(
        {
            BankAccount.balance: BankAccount.balance - a.amount,
            BankAccount.updated_at: datetime.now(),
        }
    )
    db.commit()
    return {"message": f"Withdrawn a balance of {a.amount}"}


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
