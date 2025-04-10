from api.entrypoint.user.models import Amount,UserLoginModel
from dbschemas.tables import AdminSchema, UserSchema, BankAccount


def get_user(model: UserLoginModel, db):
    user = db_admin = db.query(UserSchema).filter_by(username=model.username).first()
    return user