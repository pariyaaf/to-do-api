from db import db
from models.base_model import BaseModel


class TaskModel(BaseModel):

    __tablename__ ="tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=True)
    due_date = db.Column(db.Boolean, unique=False, nullable=True)
    priority = db.Column(db.Column(db.Integer, unique=False, default=1, nullable=False))
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String(50), nullable=True)

    list = db.relationship("UserModel", back_populates="tasks")


