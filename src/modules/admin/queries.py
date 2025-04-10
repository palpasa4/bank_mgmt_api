from dbschemas.tables import UserSchema
from src.api.entrypoint.admin.models import CreateUserModel
from dbschemas.tables import AdminSchema, UserSchema, BankAccount
from api.entrypoint.admin.models import CreateUserModel, AdminLoginModel


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
