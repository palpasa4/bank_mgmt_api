from sqlalchemy import select
from src.dbschemas import user
from src.dbschemas.tables import UserSchema
from src.api.entrypoint.admin.models import CreateUserModel
from src.dbschemas.tables import AdminSchema, UserSchema, BankAccount, Transactions
from src.api.entrypoint.admin.models import CreateUserModel, AdminLoginModel
from src.api.entrypoint.admin.responses import AdminViewDetails, AdminTransactionDetails


def get_admin(model: AdminLoginModel, db):
    admin = db_admin = db.query(AdminSchema).filter_by(username=model.username).first()
    return admin


def get_user(username: str, db):
    user = db.query(UserSchema).filter(UserSchema.username == username).first()
    return user


def add_user(model: CreateUserModel, id: str, password: str, hashed_pw: str, db):
    db_user = UserSchema(
        cust_id=id, username=model.username, password=hashed_pw, role="user"
    )
    db.add(db_user)
    db.commit()
    return db_user


def add_account(id, fullname, address, phone_number, opening_balance, new_cust, db):
    db_acc = BankAccount(
        bank_acc_id=id,
        fullname=fullname,
        address=address,
        contact_no=phone_number,
        balance=opening_balance,
        cust_id=new_cust,
    )
    db.add(db_acc)
    db.commit()


def get_details(id, db):
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
    users_list = [AdminViewDetails(**dict(detail._mapping)) for detail in details]
    return users_list


def get_transactions(id, db):
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
    transaction_list = [
        AdminTransactionDetails(**transaction) for transaction in transactions
    ]
    return transaction_list
