from data import load_json,write_json,to_dict
import uuid,json,datetime
from models import User
from fastapi import HTTPException

class Customer():
    def __init__(self,cust_id:str,username:str,password:str,role:str):
        self.cust_id=cust_id
        self.username=username
        self.password=password
        self.role=role
        
class Admin(Customer):
    def __init__(self, cust_id: str, username: str, password: str, role: str):
        super().__init__(cust_id, username, password, role)

    def create_new_user(self,newuser:User):
        cust_id=f"CUST-{str(uuid.uuid4())[:8]}"
        c=Customer(cust_id,newuser.username,newuser.password,"user")
        new_data=to_dict(c)
        data=load_json("database/user_data.json")
        data.append(new_data)
        write_json("database/user_data.json",data)          
        bank_acc_id= f"ACC-{str(uuid.uuid4())[:8]}"
        new_user={
            "bank_acc_id":bank_acc_id,
            "fullname": newuser.fullname,
            "address": newuser.address,
            "contact_no": newuser.contact_no,
            "balance": newuser.opening_balance
        }  
        data=load_json("database/bank_acc.json") 
        data.append(new_user)
        write_json("database/bank_acc.json",data)

        #store a relation: cust_id->bank_acc_id
        data=load_json("database/relation.json")
        new_relation={
            "cust_id":cust_id,
            "bank_acc_id":bank_acc_id
        }  
        data.append(new_relation) 
        write_json("database/relation.json",data) 
        return {"message": "Bank account successfully created."}


class BankAccount:
    def __init__(self,bank_id:str) -> None:
        self.bank_id=bank_id

    def deposit(self,amount:float):
        if(amount<500):
            raise HTTPException(status_code=400,detail="Minimum amount of deposit is 500. Enter amount again!")
        accounts=load_json("database/bank_acc.json")
        for account in accounts:
            if(account["bank_acc_id"]==self.bank_id): 
                prev_balance=account["balance"]            
                account["balance"]=account["balance"]+amount
                write_json("database/bank_acc.json",accounts)
                tid=f"TID-{str(uuid.uuid4())[:8]}"
                date=str(datetime.datetime.now()) 
                self.save_transaction(tid,"deposit",amount,prev_balance,account["balance"],date)
                return {"message":"Transaction saved successfully!","Transaction ID":tid,"Deposited Amount":amount,"Previous Balance":prev_balance,"New Balance":account["balance"]}

    def withdraw(self,amount:float):
        min_balance=500
        if(amount<min_balance):
            raise HTTPException(status_code=400,detail="Minimum amount of withdrawal is 500. Enter amount again!")
        accounts=load_json("database/bank_acc.json")
        for account in accounts:
            if(account["bank_acc_id"]==self.bank_id):   
                if(amount>account["balance"]-min_balance):
                    raise HTTPException(status_code=400,detail=f"No sufficient amount for withdrawal. Minimum existing balance should be NPR 500. Available Balance: {account["balance"]}")
                prev_balance=account["balance"]            
                account["balance"]=account["balance"]-amount
                write_json("database/bank_acc.json",accounts)
                tid=f"TID-{str(uuid.uuid4())[:8]}"
                date=str(datetime.datetime.now()) 
                self.save_transaction(tid,"withdrawal",amount,prev_balance,account["balance"],date)
                return {"message":"Transaction saved successfully!","Transaction ID":tid,"Deposited Amount":amount,"Previous Balance":prev_balance,"New Balance":account["balance"]}

    def save_transaction(self,tid:str,detail:str,amount:float,prev_balance:float,new_balance:float,date:str):
        record=load_json("database/transactions.json")
        new_transaction = {
            "bank_id":self.bank_id,
            "transaction_id": tid,
            "detail": detail,
            "amount": amount,
            "previous balance":prev_balance,
            "new balance":new_balance,
            "date": date 
        }
        record.append(new_transaction)
        write_json("database/transactions.json",record)