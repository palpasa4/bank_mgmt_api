from datetime import datetime
from pydantic import BaseModel


class UserViewDetails(BaseModel):
    cust_id: str
    username: str
    bank_acc_id: str
    fullname: str
    address: str
    contact_no: str
    balance: float
    updated_at: datetime


class UserTransactionDetails(BaseModel):
    transaction_id: str
    bank_acc_id: str
    transaction_type: str
    amount: float
    previous_balance: float
    new_balance: float
    timestamp: datetime
