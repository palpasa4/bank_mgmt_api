import json,uuid
from classes import Customer,Admin,BankAccount
from data import load_json,write_json,to_dict
from models import User,Login,Amount,UserDetail,TransactionDetail
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import RedirectResponse

app=FastAPI()

def validate_user_data(newuser:User):
    data=load_json("database/user_data.json")
    #Status code: 400 -> Bad Request -> Client side -> Input validation Errors
    if (any(user for user in data if user["username"] == newuser.username)):
        raise HTTPException(status_code=400, detail="Username already exists!")
    if(len(newuser.username)<7):
        raise HTTPException(status_code=400, detail="Username should contain atleast 7 characters!")
    if(newuser.opening_balance<500):
        raise HTTPException(status_code=400, detail="Minimum opening balance is 500!")


def validate_token(request:Request):
    auth_header=request.headers.get("Authorization")
    #status code 401: Authentication error, no token, mismatched credential, token expired
    if not auth_header or not auth_header.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    token=auth_header.split(" ")[1]
    admin_data=load_json("database/admin_data.json")
    user_data=load_json("database/user_data.json")
    if any(token==admin["admin_id"] for admin in admin_data):
        return [token,"admin"] 
    if any(token==user["cust_id"] for user in user_data):
        return [token,"user"]
    

#admin login
@app.post("/admin/login")
def login_admin_resource(login:Login):
    admin= load_json("database/admin_data.json")
    for data in admin:
        if (login.username == data["username"] and login.password == data["password"]):
            return {"message": "Login Success", "admin_id": data["admin_id"]}
    raise HTTPException(status_code=401, detail="Invalid username or password!")         


#admin validation and create user
@app.post("/admin/create_users")
def create_user_resource(newuser:User,request:Request):
    token=validate_token(request)
    #status_code: 401->Invalid request, 403->Forbidden (Authenticated but not authorized)
    if token is None:  
        raise HTTPException(status_code=401, detail="Invalid user. Cannot perform operation!")
    elif token[1]=="user":
        raise HTTPException(status_code=403,detail="You do not have permission to perform this operation.")
    validate_user_data(newuser)
    admin_data=load_json("database/admin_data.json")
    for admin in admin_data: 
        if(token[0]==admin["admin_id"]):
            a=Admin(admin["admin_id"],admin["username"],admin["password"],token[1])
            return a.create_new_user(newuser)  


#user login
@app.post("/user/login")
def login_user_resource(login:Login):
    user= load_json("database/user_data.json")
    for data in user:
        if (login.username==data["username"] and login.password==data["password"]):
            return {"message":"Login Success", "cust_id":data["cust_id"]}
    raise HTTPException(status_code=401,detail="Invalid username or password!")


#user: deposit
@app.post("/user/deposit")
def deposit_amount(a:Amount,request:Request):
    token=validate_token(request)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid user. Cannot perform operation!")
    elif token[1]=="admin":
        raise HTTPException(status_code=403,detail="You do not have permission to perform this operation!")
    relations=load_json("database/relation.json")
    return next((BankAccount(relation["bank_acc_id"]).deposit(a.amount) for relation in relations 
                if(relation["cust_id"]==token[0])),None)
#next(iterator, default)


#user: withdraw
@app.post("/user/withdraw")
def withdraw_amount(a:Amount,request:Request):
    token=validate_token(request)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid user. Cannot perform operation!")
    elif token[1]=="admin":
        raise HTTPException(status_code=403,detail="You do not have permission to perform this operation!")
    relations=load_json("database/relation.json")
    return next((BankAccount(relation["bank_acc_id"]).withdraw(a.amount) for relation in relations 
                if(relation["cust_id"] == token[0])),None)


#view details
@app.get("/details")
def view_details(request:Request):
    token=validate_token(request)
    if token is None:
        raise HTTPException(status_code=401,detail="Invalid User. Cannot perform operation!")
    user_data =  load_json("database/user_data.json")
    acc_data=load_json("database/bank_acc.json")
    if(len(user_data) != len(acc_data)):
        raise HTTPException(status_code=400,detail="Mismatched no of data in user details and bank acc!")
    merged_data = [{**d1, **d2} for d1, d2 in zip(user_data, acc_data)]     # Merge corresponding elements in a single list
    filtered_data = [UserDetail(**item) for item in merged_data]    #a new list:filter using BaseModel
    if(token[1]=="admin"):
        return {"User Details":filtered_data}
    user_detail=[data for data in merged_data if token[0]==data["cust_id"] ]
    return {"User Details":user_detail[0]}
            

#view transactions
@app.get("/transactions")
def view_transactions(request:Request):
    token=validate_token(request)
    if token is None:
        raise HTTPException(status_code=401,detail="Invalid User. Cannot perform operation!")
    transactions=load_json("database/transactions.json")
    if(token[1]=="admin"):
        transactions=[TransactionDetail(**transaction) for transaction in transactions]
        return {"Transaction details": transactions}   
    relations=load_json("database/relation.json")
    bank_id=[relation["bank_acc_id"] for relation in relations if token[0]==relation["cust_id"]]
    transactions=[transaction for transaction in transactions if bank_id[0]==transaction["bank_id"]]
    return{"Transaction details":transactions} #consistency while displaying o/p!

#encryption while storing in database.