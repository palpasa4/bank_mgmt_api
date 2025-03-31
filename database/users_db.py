import uuid
from database.tables import UserSchema,BankAccount
from core.auth.auth_handler import hash_password
from models.request_models import Login,User,Amount
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database.conn import get_db

def add_newuser(newuser,db:Session=Depends(get_db)):
    new_id=f"CUST-{str(uuid.uuid4())[:8]}"
    hashed_pw = hash_password(newuser.password)
    db_user = UserSchema(cust_id=new_id,username=newuser.username, password=hashed_pw,role="user")
    db.add(db_user)
    db.commit()

def create_bank_acc(newuser:User,db:Session=Depends(get_db)):
    new_bankid=f"ACC-{str(uuid.uuid4())[:8]}"
    db_acc=BankAccount(bank_acc_id=new_bankid,fullname=newuser.fullname,address=newuser.address,contact_no=newuser.contact_no,balance=newuser.opening_balance)
    db.add(db_acc)
    db.commit()

def deposit(a:Amount):
    pass