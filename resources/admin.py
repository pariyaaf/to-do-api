from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.user import UserSchema
from models import UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify  
from sqlalchemy import text  

blp = Blueprint("Admins", "admins", description="Operations on users")

@blp.route("/admin/users")
class Admin(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        current_user = UserModel.query.get(get_jwt_identity())

        if current_user.is_admin == 1:
            users =  UserModel.query.all()
            return users
        
        abort(403, message="Dont have permission to access !")

    

@blp.route("/admin/db")
class CheckMigration(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema())
    def get(self):
        try:
            result = db.session.execute(text("SELECT * FROM alembic_version"))
            rows = [dict(row._mapping) for row in result]  # استفاده از _mapping
            return jsonify(rows)
        except Exception as e:
            return jsonify({"error": str(e)}), 500