from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, func
from psycopg2.errors import UniqueViolation
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from src.core.extensions.conn import Base


class AdminSchema(Base):
    __tablename__ = "admin_data"

    admin_id = Column(String, primary_key=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    role = Column(String, index=True)


class UserSchema(Base):
    __tablename__ = "user_data"

    cust_id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    role = Column(String, index=True)


class BankAccount(Base):
    __tablename__ = "bank_acc"

    bank_acc_id = Column(String, primary_key=True, index=True)
    fullname = Column(String, index=True)
    address = Column(String, index=True)
    contact_no = Column(String, index=True)
    balance = Column(Float, index=True)
    cust_id = Column(String, ForeignKey("user_data.cust_id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now())


class Transactions(Base):
    __tablename__ = "transaction_history"

    transaction_id = Column(String, primary_key=True, index=True)
    bank_acc_id = Column(String, ForeignKey("bank_acc.bank_acc_id"), nullable=False)
    transaction_type = Column(String, index=True)
    amount = Column(Float, index=True)
    previous_balance = Column(Float, index=True)
    new_balance = Column(Float, index=True)
    timestamp = Column(DateTime)
