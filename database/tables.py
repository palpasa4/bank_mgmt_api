from sqlalchemy import Column, Integer, String,Float,Date
from psycopg2.errors import UniqueViolation
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

#Base models
class AdminSchema(Base):
    __tablename__='admin_data'

    admin_id=Column(String,primary_key=True,index=True)
    username=Column(String,index=True)
    password=Column(String,index=True)
    role=Column(String,index=True)

class UserSchema(Base):
    __tablename__='user_data'

    cust_id=Column(String,primary_key=True,index=True)
    username=Column(String,index=True)
    password= Column(String,index=True)
    role=Column(String,index=True)

class BankAccount(Base):
    __tablename__='bank_acc'

    bank_acc_id=Column(String,primary_key=True,index=True)
    fullname=Column(String,index=True)
    address=Column(String,index=True)
    contact_no=Column(String,index=True)
    balance=Column(Float,index=True)

# class Relation(Base):
#     __tablename__='relation'

#     cust_id=Column(String,index=True)
#     bank_acc_id=Column(String,index=True)

# class Transactions(Base):
#     __tablename__='transactions'

#     bank_id=Column(String,index=True)
#     transaction_id=Column(String,index=True)
#     detail=Column(String,index=True)
#     amount=Column(Float,index=True)
#     previous_balance=Column(Float,index=True)
#     new_balance=Column(Float,index=True)
#     date=Column(Date,index=True)