from db import db
from models.base_model import BaseModel


class UserModel(BaseModel):

    __tablename__ ="users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, nullable=False)


