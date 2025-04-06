from fastapi import APIRouter, Depends, HTTPException
from database.tables import AdminSchema, UserSchema
from models.request_models import Login, User
from core.handlers.response_handler import json_response
from core.auth.auth_handler import sign_jwt
from core.auth.helpers import check_password, check_role
from core.auth.auth_bearer import JWTBearer
from core.handlers.logger_config import logger
from database.conn import db_dependency
from database.users_db import add_newuser

router = APIRouter()


# admin login
@router.post("/admin/login")
async def admin_login(admin: Login, db: db_dependency):
    logger.info("Admin login page was accessed.")
    db_admin = db.query(AdminSchema).filter_by(username=admin.username).first()
    if db_admin is None or not check_password(admin.password, str(db_admin.password)):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return sign_jwt(str(db_admin.admin_id))


# admin validation and create user
@router.post("/admin/create_users", tags=["create_users"])
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
