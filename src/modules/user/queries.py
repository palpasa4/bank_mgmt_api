from api.entrypoint.user.models import Amount,UserLoginModel
from dbschemas.tables import AdminSchema, UserSchema, BankAccount
from datetime import datetime


def get_user(model: UserLoginModel, db):
    user = db_admin = db.query(UserSchema).filter_by(username=model.username).first()
    return user


def add_balance(model:Amount,id:str,db):
    db.query(BankAccount).filter(BankAccount.cust_id == id).update(
        {
            BankAccount.balance: BankAccount.balance + model.amount,
            BankAccount.updated_at: datetime.now(),
        }
    )
    db.commit()
    return BankAccount