import uuid
from datetime import datetime
from sqlalchemy import desc, select
from database.tables import UserSchema, BankAccount, Transactions
from core.auth.helpers import hash_password
from models.request_models import Login, User, Amount
from models.admin_response import AdminViewDetails, AdminTransactionDetails
from models.user_response import UserViewDetails, UserTransactionDetails
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database.conn import get_db
from returns.result import safe,Success,Failure


def add_newuser(newuser, db):
    new_cust_id = f"CUST-{str(uuid.uuid4())[:8]}"
    hashed_pw = hash_password(newuser.password)
    db_user = UserSchema(
        cust_id=new_cust_id, username=newuser.username, password=hashed_pw, role="user"
    )
    db.add(db_user)
    db.commit()
    create_bank_acc(newuser, new_cust_id, db)
    return {"message":"Bank acc created successfully!"}


def create_bank_acc(newuser: User, new_cust, db: Session = Depends(get_db)):
    new_bankid = f"ACC-{str(uuid.uuid4())[:8]}"
    db_acc = BankAccount(
        bank_acc_id=new_bankid,
        fullname=newuser.fullname,
        address=newuser.address,
        contact_no=newuser.contact_no,
        balance=newuser.opening_balance,
        cust_id=new_cust,
    )
    db.add(db_acc)
    db.commit()


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


def admin_view_details(db: Session = Depends(get_db)):
    details = db.execute(
        select(
            UserSchema.cust_id,
            UserSchema.username,
            BankAccount.bank_acc_id,
            BankAccount.fullname,
            BankAccount.address,
            BankAccount.contact_no,
            BankAccount.created_at,
            BankAccount.updated_at,
        ).outerjoin(BankAccount, UserSchema.cust_id == BankAccount.cust_id)
    ).fetchall()
    if not details:
        return {"error": "No data found."}
    users_list = [AdminViewDetails(**dict(detail._mapping)) for detail in details]
    return {"details": users_list}


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


def admin_view_transactions(db: Session = Depends(get_db)):
    transactions = (
        db.execute(
            select(
                Transactions.transaction_id,
                Transactions.bank_acc_id,
                Transactions.transaction_type,
                Transactions.amount,
                Transactions.timestamp,
            )
        )
        .mappings()
        .all()
    )
    if not transactions:
        return {"error": "No transactions found."}
    transaction_list = [
        AdminTransactionDetails(**transaction) for transaction in transactions
    ]
    return {"transactions": transaction_list}


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
