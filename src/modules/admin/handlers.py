import stat
import uuid, hashlib
from sqlalchemy import select
from src.dbschemas.tables import UserSchema, BankAccount, Transactions
from src.core.auth.helpers import hash_password, check_password, check_role
from src.api.entrypoint.admin.models import CreateUserModel, AdminLoginModel
from src.api.dependencies import AnnotatedDatabaseSession
from src.api.entrypoint.admin.responses import AdminViewDetails, AdminTransactionDetails
from fastapi import Depends
from sqlalchemy.orm import Session
from src.api.dependencies import get_db_session
from src.modules.admin.queries import (
    add_user,
    get_user,
    get_admin,
    add_account,
    get_details,
    get_transactions,
)
from src.core.logconfig import logger
from src.modules.admin.exceptions import *
from src.modules.user.exceptions import *
from src.core.exceptions import *


def check_valid_admin(model: AdminLoginModel, db:AnnotatedDatabaseSession):
    admin = get_admin(model, db)
    if admin is None or not check_password(
        model.password.get_secret_value(), str(admin.password)
    ):
        logger.warning(
            f"Failed admin login attempt: Username: {model.username} Password:{model.password}"
        )
        raise InvalidAdminLoginException(
            message=f"Login Failed: Invalid username or password.", status_code=401
        )
    return admin


def check_ifadmin(id: str, db:AnnotatedDatabaseSession):
    if check_role(id, db) != "admin":
        logger.error(f"Unauthorized access attempt by user {id}")
        raise UserPermissionDeniedException(
            message="User not allowed.", status_code=401
        )


def check_user_details(model: CreateUserModel):
    if len(model.username) < 7:
        # simple input validation issue
        logger.warning("Username too short: must be at least 7 characters long")
        raise ValidationException(
            message="Username must be at least 7 characters long!", status_code=400
        )

    if len(model.username) > 20:
        logger.warning("Username too long: cannot be more than 20 characters!")
        raise ValidationException(
            message="Username cannot include more than 20 characters!", status_code=400
        )

    if model.opening_balance < 500:
        # business rule violation
        logger.error(
            "Bank account creation failed: opening balance below minimum requirement"
        )
        raise ValidationException(
            message="Minimum opening balance is 500!", status_code=400
        )


def check_duplicate_user(username: str, db:AnnotatedDatabaseSession):
    user = get_user(username, db)
    if user:
        logger.error("Admin attempted to create a user with an existing username")
        raise DuplicateUserException(
            message=f"User with username {username} already exists.", status_code=409
        )


def create_user(model: CreateUserModel, db:AnnotatedDatabaseSession):
    try:
        new_cust_id = f"CUST-{str(uuid.uuid4())[:8]}"
        password = hashlib.sha256(model.username.encode()).hexdigest()[:12]
        hashed_pw = hash_password(password)
        add_user(model, new_cust_id, password, hashed_pw, db)
        create_bank_acc(model, new_cust_id, db)
    except Exception as e:
        logger.error(
            f"Database error: Unable to add user '{model.username}' to table 'user_data'.Error: {str(e)}"
        )
        raise DatabaseException("Database error: Unable to add user.", status_code=500)


def create_bank_acc(model: CreateUserModel, new_cust, db:AnnotatedDatabaseSession):
    try:
        new_bankid = f"ACC-{str(uuid.uuid4())[:8]}"
        add_account(
            new_bankid,
            model.fullname,
            model.address,
            model.phone_number,
            model.opening_balance,
            new_cust,
            db,
        )
    except Exception as e:
        logger.error(
            f"Database error: Unable to create bank_acc for '{model.username}'.Error: {str(e)}"
        )
        raise DatabaseException(
            "Database error: Unable to create bank account.", status_code=500
        )


# remaining work
def admin_view_details(db: AnnotatedDatabaseSession):
    users_list = get_details(id, db)
    if not users_list:
        logger.error("Database Exception: No details found!")
        raise DetailNotFoundException(message="No details found!", status_code=404)
    return users_list


def admin_view_specific_detail(db: AnnotatedDatabaseSession):
    pass


def admin_view_transactions(db: AnnotatedDatabaseSession):
    transaction_list = get_transactions(id, db)
    if not transaction_list:
        logger.error("Database Error: No transactions found. ")
        raise TransactionsNotFoundException(
            message="No transactions found!", status_code=404
        )
    return transaction_list
