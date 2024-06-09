from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.user import UserSchema
from models import UserModel
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request 
from sqlalchemy import text 
from datetime import datetime

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

    
@blp.route("/admin/user")
class Admin(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema())
    def post(self):

        admin_id = get_jwt_identity()
        admin = UserModel.query.get_or_404(admin_id)

        if admin.is_admin:
            data = request.get_json()
            user_id = data.get('user_id')
            is_admin = data.get('is_admin')
            user = UserModel.query.get_or_404(user_id)

            try:
                if user:
                    user.is_admin = bool(is_admin)
                    user.updated = datetime.utcnow(),
                    db.session.add(user)
                    db.session.commit()
                    return user

            except Exception as e:
                abort(500, message=f"error => {e} !")

        else:
            abort(403, message=" You dont have permission!")

    
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
            abort(500, message=f"error => {e} !")
