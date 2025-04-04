from database.tables import AdminSchema, UserSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from database.conn import init_db, get_db
from models.request_models import Login, User, Amount
from fastapi import Depends, FastAPI, HTTPException, Request, Body
from typing import Annotated
from core.handlers.response_handler import json_response
from core.auth.auth_handler import sign_jwt
from core.auth.helpers import check_password, check_role
from core.auth.auth_bearer import JWTBearer
from database.users_db import (
    add_newuser,
    create_bank_acc,
    deposit,
    withdraw,
    admin_view_details,
    user_view_details,
    admin_view_transactions,
    user_view_transactions,
)

app = FastAPI()

init_db()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/admin/login")
async def admin_login(admin: Login, db: db_dependency):
    db_admin = db.query(AdminSchema).filter_by(username=admin.username).first()
    if db_admin is None or not check_password(admin.password, str(db_admin.password)):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return sign_jwt(str(db_admin.admin_id))


# admin validation and create user
@app.post("/admin/create_users", tags=["create_users"])
def create_user_resource(
    newuser: User, db: db_dependency, user_id: str = Depends(JWTBearer())
):
    if check_role(user_id, db) != "admin":
        raise HTTPException(status_code=403, detail="User not allowed!")
    existing_user = (
        db.query(UserSchema).filter(UserSchema.username == newuser.username).first()
    )
    # check for exceptions: username less than 7 characters, same uname,
    print(existing_user)  # raise UsernameAlreadyExists() : Middleware
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists!")
    if newuser.opening_balance < 500:
        raise HTTPException(status_code=400, detail="Minimum opening balance is 500!")
    add_newuser(newuser, db)
    return {"message": "Bank acc created successfully!"}


# user login
@app.post("/user/login")
async def user_login(user: Login, db: db_dependency):
    db_user = db.query(UserSchema).filter_by(username=user.username).first()
    if db_user is None or not check_password(user.password, str(db_user.password)):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return sign_jwt(str(db_user.cust_id))


# user: deposit
@app.post("/user/deposit", tags=["user_deposit"])
def deposit_amount(
    a: Amount, db: db_dependency, user_id: str = Depends(JWTBearer())
):  # use of depends?
    if check_role(user_id, db) != "user":
        raise HTTPException(status_code=403, detail="User not allowed!")
    if a.amount < 500:
        raise HTTPException(status_code=400, detail="Minimum amount of deposit is 500!")
    return deposit(a, user_id, db)


# user: withdraw
@app.post("/user/withdraw")
def withdraw_amount(a: Amount, db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) != "user":
        raise HTTPException(status_code=403, detail="User not allowed!")
    if a.amount < 500:
        raise HTTPException(
            status_code=400, detail="Minimum amount of withdrawal is 500!"
        )
    return withdraw(a, user_id, db)


# view details
@app.get("/details")
def view_details(db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) == "admin":
        return admin_view_details(db)
    return user_view_details(user_id, db)


# view transactions
@app.get("/transactions")
def view_transactions(db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) == "admin":
        return admin_view_transactions(db)
    return user_view_transactions(user_id, db)
