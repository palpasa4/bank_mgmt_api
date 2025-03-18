import json,uuid
from classes import Customer,Admin,BankAccount
from data import load_json,write_json,to_dict
from models import User,Login,Amount,UserDetail,TransactionDetail
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import RedirectResponse

app=FastAPI()

def validate_token(request:Request):
    auth_header=request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        print("No token received!")
        raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    token=auth_header.split(" ")[1]
    admin_data=load_json("database/admin_data.json")
    for user in admin_data:
        if(token==user["admin_id"]):
            return [token,"admin"]
    user_data=load_json("database/user_data.json")
    for user in user_data:
        if(token==user["cust_id"]):
            return [token,"user"]

#encryption while storing in database.

#admin login
@app.post("/admin/login")
def login_admin_resource(login:Login):
    user= load_json("database/admin_data.json")
    for data in user:
        if(login.username==data["username"] and login.password==data["password"]):
            return {"message":"Login Success", "admin_id":data["admin_id"]}
    return{"Error":"Invalid Credentials."}


#admin validation and create user
@app.post("/admin/create_users")
def create_user_resource(newuser:User,request:Request):
    token=validate_token(request)
    if token is not None:  
        admin_data=load_json("database/admin_data.json")
        for user in admin_data:
            if(token[0]==user["admin_id"]):
                data=load_json("database/user_data.json")
                if (any(user for user in data if user["username"] == newuser.username)):
                    return {"message":"Error creating user. Enter details again."}
                else:
                    cust_id=f"CUST-{str(uuid.uuid4())[:8]}"
                    c=Customer(cust_id,newuser.username,newuser.password,"user")
                    new_data=to_dict(c)
                    data.append(new_data)
                    write_json("database/user_data.json",data)          
                    if(newuser.opening_balance<500):
                        return {"message":"Minimum opening balance is 500!"}
                    else:
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
    return{"Error":"Invalid User. Cannot perform operation!"}


#user login
@app.post("/user/login")
def login_user_resource(login:Login):
    user= load_json("database/user_data.json")
    for data in user:
        if(login.username==data["username"] and login.password==data["password"]):
            return {"message":"Login Success", "cust_id":data["cust_id"]}
    return{"Error":"Invalid Credentials."}


#user: deposit
@app.post("/user/deposit")
def deposit_amount(a:Amount,request:Request):
    token=validate_token(request)
    if token is not None:
        relations=load_json("database/relation.json")
        for relation in relations:
            if(relation["cust_id"]==token[0]):
                return BankAccount(relation["bank_acc_id"]).deposit(a.amount)
    return{"Error":"Invalid User. Cannot perform deposit."}


#user: withdraw
@app.post("/user/withdraw")
def withdraw_amount(a:Amount,request:Request):
    token=validate_token(request)
    if token is not None:
        relations=load_json("database/relation.json")
        for relation in relations:
            if(relation["cust_id"]==token[0]):
                return BankAccount(relation["bank_acc_id"]).withdraw(a.amount)
    return {"Error":"Invalid User. Cannot perform deposit."}


#view details
@app.get("/details")
def view_details(request:Request):
    token=validate_token(request)
    if token is not None:
        user_data =  load_json("database/user_data.json")
        acc_data=load_json("database/bank_acc.json")
        if(len(user_data) == len(acc_data)):
            print("Same no of elements.")
            # Merge corresponding elements in a single list
            merged_data = [{**d1, **d2} for d1, d2 in zip(user_data, acc_data)]
            #create a new list with filetered data using the BaseModel
            filtered_data = [UserDetail(**item) for item in merged_data]
            if(token[1]=="admin"):
                return {"User Details":filtered_data}
            else:
                user_detail=[data for data in merged_data if token[0]==data["cust_id"] ]
                return {"Your Details":user_detail[0]}
        else:
            raise HTTPException(status_code=400,detail="Mismatched length of lists!")
            
    raise HTTPException(status_code=401,detail="Invalid User. Cannot view details!")


#view transactions
@app.get("/transactions")
def view_transactions(request:Request):
    token=validate_token(request)
    if token is not None:
        transactions=load_json("database/transactions.json")
        if(token[1]=="admin"):
            transactions=[TransactionDetail(**transaction) for transaction in transactions]
            if transactions:
                return {"Transaction details": transactions}
            else:
                return {"Message":"No transactions made."}
            
        else:
            relations=load_json("database/relation.json")
            bank_id=[relation["bank_acc_id"] for relation in relations if token[0]==relation["cust_id"]]
            transactions=[transaction for transaction in transactions if bank_id[0]==transaction["bank_id"]]
            if(transactions):
                return{"Transaction details":transactions}
            else:
                return{"Message":"No transactions made."}
    raise HTTPException(status_code=401,detail="Invalid User. Cannot view details!")