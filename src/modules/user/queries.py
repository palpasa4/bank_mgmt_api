from api.entrypoint.user.models import Amount, UserLoginModel
from dbschemas.tables import AdminSchema, UserSchema, BankAccount
from datetime import datetime


def get_user(model: UserLoginModel, db):
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
