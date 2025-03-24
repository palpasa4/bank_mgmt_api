from pydantic import BaseModel

class Login(BaseModel):
    username:str
    password:str

class User(BaseModel):
    username:str
    password:str
    fullname:str
    address:str
    contact_no:str
    opening_balance:float

class Amount(BaseModel):
    amount:float

class UserDetail(BaseModel):
    username:str
    fullname:str
    address:str
    contact_no:str

class TransactionDetail(BaseModel):
    transaction_id:str
    detail:str
    amount:float
    date:str