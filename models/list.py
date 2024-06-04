from db import db
from models.base_model import BaseModel


class ListModel(BaseModel):

    __tablename__ ="lists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    color = db.Column(db.String(120), unique=False, nullable=True)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    tasks = db.relationship("TaskModel", back_populates="list", lazy='dynamic',cascade="all, delete")




