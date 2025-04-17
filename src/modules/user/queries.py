from typing import Optional
from src.api.entrypoint.user.models import Amount, UserLoginModel
from src.dbschemas.tables import AdminSchema, UserSchema, BankAccount, Transactions
from src.api.dependencies import AnnotatedDatabaseSession
from datetime import datetime
from sqlalchemy import select


def get_user(model: UserLoginModel, db: AnnotatedDatabaseSession):
    user = db_admin = db.query(UserSchema).filter_by(username=model.username).first()
    return user


def add_balance(model: Amount, id: str, db):
    account = db.query(BankAccount).filter(BankAccount.cust_id == id).first()
    if account:
        account.balance += model.amount
        account.updated_at = datetime.now()
        db.commit()
    return account


def deduct_balance(model: Amount, id: str, db):
    account = db.query(BankAccount).filter(BankAccount.cust_id == id).first()
    if account:
        account.balance -= model.amount
        account.updated_at = datetime.now()
        db.commit()
    return account


def get_detail(id: str, db):
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
        .where(UserSchema.cust_id == id)
    ).fetchone()
    return details


def get_transactions(id: str, db):
    bank_acc_id = db.execute(
        select(BankAccount.bank_acc_id).where(BankAccount.cust_id == id)
    ).scalar()
    transactions = db.execute(
        select(Transactions).where(Transactions.bank_acc_id == bank_acc_id)
    ).fetchall()
    return transactions
