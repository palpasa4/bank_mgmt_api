from data import load_json,write_json
import uuid,json,datetime

class Customer():

    def __init__(self,cust_id:str,username:str,password:str,role:str):
        self.cust_id=cust_id
        self.username=username
        self.password=password
        self.role=role
        
class Admin(Customer):

    def __init__(self, cust_id: str, username: str, password: str, role: str):
        super().__init__(cust_id, username, password, role)

class BankAccount:
    def __init__(self,bank_id:str) -> None:
        self.bank_id=bank_id

    def deposit(self,amount:float):
        if(amount<500):
            return {"Error":"Minimum amount of deposit is 500. Enter amount again!"}
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
            return {"Error":"Minimum amount of withdrawal is 500. Enter amount again!"}
        accounts=load_json("database/bank_acc.json")
        for account in accounts:
            if(account["bank_acc_id"]==self.bank_id):   
                if(amount<=account["balance"]-min_balance):
                    prev_balance=account["balance"]            
                    account["balance"]=account["balance"]-amount
                    write_json("database/bank_acc.json",accounts)
                    tid=f"TID-{str(uuid.uuid4())[:8]}"
                    date=str(datetime.datetime.now()) 
                    self.save_transaction(tid,"withdrawal",amount,prev_balance,account["balance"],date)
                    return {"message":"Transaction saved successfully!","Transaction ID":tid,"Deposited Amount":amount,"Previous Balance":prev_balance,"New Balance":account["balance"]}
                else:
                    return {"Error":"No sufficient amount for withdrawal. Minimum existing balance should be NPR 500. ", "Available Balance": account["balance"]}
        
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