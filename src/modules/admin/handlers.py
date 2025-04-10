import uuid, hashlib
from sqlalchemy import select
from dbschemas.tables import UserSchema, BankAccount, Transactions
from core.auth.helpers import hash_password, check_password, check_role
from api.entrypoint.admin.models import CreateUserModel, AdminLoginModel
from api.entrypoint.admin.responses import AdminViewDetails, AdminTransactionDetails
from fastapi import Depends
from sqlalchemy.orm import Session
from src.api.dependencies import get_db
from modules.admin.queries import add_user, get_user, get_admin, add_account
from core.logconfig import logger
from src.modules.admin.exceptions import *
from src.modules.user.exceptions import *
from src.core.handlers.exceptions import *


def check_valid_admin(model: AdminLoginModel, db):
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


def check_ifadmin(id: str, db):
    if check_role(id, db) != "admin":
        logger.error(f"Unauthorized access attempt by user {id}")
        raise UserPermissionDeniedException(
            message="User not allowed.", status_code=401
        )


def check_user_details(model: CreateUserModel):
    if len(model.username) < 7:
        # simple input validation issue
        logger.warning("Username too short: must be at least 7 characters long")
        raise UsernameTooShortException(
            message="Username must be at least 7 characters long!", status_code=400
        )

    if len(model.username) > 20:
        logger.warning("Username too long: cannot be more than 20 characters!")
        raise UsernameTooLongException(
            message="Username cannot include more than 20 characters!", status_code=400
        )

    if model.opening_balance < 500:
        # business rule violation
        logger.error(
            "Bank account creation failed: opening balance below minimum requirement"
        )
        raise OpeningBalanceException(
            message="Minimum opening balance is 500!", status_code=400
        )


def check_duplicate_user(username: str, db):
    user = get_user(username, db)
    if user:
        logger.error("Admin attempted to create a user with an existing username")
        raise DuplicateUserException(
            message=f"User with username {username} already exists."
        )


def create_user(model: CreateUserModel, db):
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


def create_bank_acc(model: CreateUserModel, new_cust, db):
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
def admin_view_details(db: Session = Depends(get_db)):
    details = db.execute(
        select(
            UserSchema.cust_id,
            UserSchema.username,
            BankAccount.bank_acc_id,
            BankAccount.fullname,
            BankAccount.address,
            BankAccount.contact_no,
            BankAccount.created_at,
            BankAccount.updated_at,
        ).outerjoin(BankAccount, UserSchema.cust_id == BankAccount.cust_id)
    ).fetchall()
    if not details:
        return {"error": "No data found."}
    users_list = [AdminViewDetails(**dict(detail._mapping)) for detail in details]
    return {"details": users_list}


def admin_view_transactions(db: Session = Depends(get_db)):
    transactions = (
        db.execute(
            select(
                Transactions.transaction_id,
                Transactions.bank_acc_id,
                Transactions.transaction_type,
                Transactions.amount,
                Transactions.timestamp,
            )
        )
        .mappings()
        .all()
    )
    if not transactions:
        return {"error": "No transactions found."}
    transaction_list = [
        AdminTransactionDetails(**transaction) for transaction in transactions
    ]
    return {"transactions": transaction_list}
