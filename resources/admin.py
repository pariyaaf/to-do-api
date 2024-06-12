from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.user import UserSchema
from models import UserModel
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request 
from sqlalchemy import text 
from datetime import datetime
from public_methods import str_to_bool

blp = Blueprint("Admins", "admins", description="Operations on users")

@blp.route("/admin/users")
class Admin(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        current_user = UserModel.get_or_404(get_jwt_identity())

        if current_user.is_admin == 1:
            param_1 = request.args.get('with_deleted', 'false')
            with_deleted = str_to_bool(param_1)
            users = UserModel.all(with_deleted=with_deleted)
            return users
        
        abort(403, message="Dont have permission to access !")

    
@blp.route("/admin/user/<int:user_id>")
class Admin(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema())
    def get(self, user_id):
        current_user = UserModel.get_or_404(get_jwt_identity())

        if current_user.is_admin == 1:
            param_1 = request.args.get('with_deleted', 'false')
            with_deleted = str_to_bool(param_1)
            user = UserModel.get_or_404(user_id, with_deleted=with_deleted)
            return user
        
        abort(403, message="Dont have permission to access !")


    @jwt_required(refresh=True)
    @blp.response(200, UserSchema())
    def put(self, user_id):
        admin_id = get_jwt_identity()
        admin = UserModel.get_or_404(admin_id)

        if admin.is_admin:
            data = request.get_json()
            is_admin = data.get('is_admin')

            param_1 = request.args.get('with_deleted', 'false')
            with_deleted = str_to_bool(param_1)

            user = UserModel.get_or_404(user_id, with_deleted=with_deleted)

            try:
                if user:
                    user.is_admin = bool(is_admin)
                    UserModel.update_record(user, admin_id)
                    return user

            except Exception as e:
                abort(500, message=f"error => {e} !")

        else:
            abort(403, message=" You dont have permission!")


    @jwt_required(refresh=True)
    @blp.response(200, UserSchema())
    def post(self, user_id):
        admin_id = get_jwt_identity()
        admin = UserModel.get_or_404(admin_id)
        user = UserModel.get(user_id, with_deleted=True)
        if admin.is_admin:
            if user and user.deleted_at is not None:
                try:
                    UserModel.restore(user, admin_id)
                    return user
                except Exception as e:
                    abort(500, message=f"error => {e} !")
            else:
                abort(400, message=" User is already exist or not found!")
        else:
            abort(403, message=" You dont have Permission!")


    @jwt_required(refresh=True)
    def delete(self, user_id):  
        admin_id = get_jwt_identity()
        admin = UserModel.get_or_404(admin_id)
        user = UserModel.get(user_id)
        if admin.is_admin:

            if user:
                try:
                    UserModel.soft_delete(user, admin_id)
                    return {"message": f"user {user.username} deleted successfully"}
                except Exception as e:
                    abort(500, message=f"error => {e} !")

            else:
                abort(400, message=" User is already deleted or not found!")
        else:
            abort(403, message=" You dont have Permission!")


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
