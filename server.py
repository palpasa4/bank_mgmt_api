from database.tables import AdminSchema, UserSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from database.conn import init_db, get_db
from models.request_models import Login,User,Amount
from fastapi import Depends, FastAPI, HTTPException, Request, Body
from typing import Annotated
from core.response_handler import json_response
from core.auth.auth_handler import check_password,sign_jwt
from core.auth.auth_bearer import JWTBearer
from database.users_db import add_newuser,create_bank_acc,deposit

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
async def admin_login(admin:Login,db:db_dependency):
    db_admin = db.query(AdminSchema).filter_by(username=admin.username).first()
    if db_admin is None or not check_password(admin.password,str(db_admin.password)): 
        raise HTTPException(status_code=401, detail="Invalid username or password")  
    return sign_jwt(str(db_admin.admin_id))
     

#admin validation and create user
@app.post("/admin/create_users",dependencies=[Depends(JWTBearer())],tags=["create_users"])
def create_user_resource(newuser:User, db: db_dependency):
    existing_user = db.query(UserSchema).filter(UserSchema.username == newuser.username).first()
    #check for exceptions: username less than 7 characters, same uname,
    if existing_user:
        # raise UsernameAlreadyExists() 
        raise HTTPException(status_code=400,detail="Username already exists!")
    if(newuser.opening_balance<500):
        raise HTTPException(status_code=400, detail="Minimum opening balance is 500!")
    add_newuser(newuser,db)
    create_bank_acc(newuser,db) 
    return {"message":"Bank acc created successfully!"}


@app.post("/user/login")
async def user_login(user:Login,db:db_dependency):
    db_user = db.query(UserSchema).filter_by(username=user.username).first()
    if db_user is None or not check_password(user.password,str(db_user.password)): 
        raise HTTPException(status_code=401, detail="Invalid username or password")  
    return sign_jwt(str(db_user.cust_id))


#user: deposit
@app.post("/user/deposit",dependencies=[Depends(JWTBearer())],tags=["user_deposit"])
def deposit_amount(a:Amount,request:Request):
    return deposit(a)


# #user: withdraw
# @app.post("/user/withdraw")
# def withdraw_amount(a:Amount,request:Request):
#     token=validate_token(request)
#     if token is None:
#         raise HTTPException(status_code=401, detail="Invalid user. Cannot perform operation!")
#     elif token[1]=="admin":
#         raise HTTPException(status_code=403,detail="You do not have permission to perform this operation!")
#     relations=load_json("database/relation.json")
#     return next((BankAccount(relation["bank_acc_id"]).withdraw(a.amount) for relation in relations 
#                 if(relation["cust_id"] == token[0])),None)


# #view details
# @app.get("/details")
# def view_details(request:Request):
#     token=validate_token(request)
#     if token is None:
#         raise HTTPException(status_code=401,detail="Invalid User. Cannot perform operation!")
#     user_data =  load_json("database/user_data.json")
#     acc_data=load_json("database/bank_acc.json")
#     if(len(user_data) != len(acc_data)):
#         raise HTTPException(status_code=400,detail="Mismatched no of data in user details and bank acc!")
#     merged_data = [{**d1, **d2} for d1, d2 in zip(user_data, acc_data)]     # Merge corresponding elements in a single list
#     filtered_data = [UserDetail(**item) for item in merged_data]    #a new list:filter using BaseModel
#     if(token[1]=="admin"):
#         return {"User Details":filtered_data}
#     user_detail=[data for data in merged_data if token[0]==data["cust_id"] ]
#     return {"User Details":user_detail[0]}
            

# #view transactions
# @app.get("/transactions")
# def view_transactions(request:Request):
#     token=validate_token(request)
#     if token is None:
#         raise HTTPException(status_code=401,detail="Invalid User. Cannot perform operation!")
#     transactions=load_json("database/transactions.json")
#     if(token[1]=="admin"):
#         transactions=[TransactionDetail(**transaction) for transaction in transactions]
#         return {"Transaction details": transactions}   
#     relations=load_json("database/relation.json")
#     bank_id=[relation["bank_acc_id"] for relation in relations if token[0]==relation["cust_id"]]
#     transactions=[transaction for transaction in transactions if bank_id[0]==transaction["bank_id"]]
#     return{"Transaction details":transactions} #consistency while displaying o/p!

# #encryption while storing in database.