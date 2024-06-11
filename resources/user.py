from flask.views import MethodView
from flask_smorest import Blueprint, abort, current_api
from schemas.user import UserSchema, UserUpdateSchema, PassUpdateSchema
from models import UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity, create_refresh_token
from datetime import datetime
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/user/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    # @blp.response(201, UserSchema)
    def post(cls, user_data):
        if UserModel.filter(UserModel.username == user_data["username"], with_deleted=True).first():
            abort(409, message="username is already exists!")

        user = UserModel(
            username = user_data["username"],
            name =   user_data["name"] if "name" in user_data else None,
            email = user_data["email"],
            password = pbkdf2_sha256.hash(str(user_data["password"])),
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow(),
            is_admin = bool(user_data["is_admin"]) if "is_admin" in user_data else False,
        )

        try:
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            abort(400, message="user already exists!")

        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the new data!")

        return {"message": "user created successfully"}, 201  


@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(cls, user_data):
        user = UserModel.filter(user_data["username"] == UserModel.username).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token" : access_token, "refresh_token" : refresh_token}

        abort(401, message="invalid data")



@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        jti = (get_jwt)()["jti"]
        BLOCKLIST.add(jti)
        return {"message" : "successfully logged out"}, 200


@blp.route("/user/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_refresh_token(identity=current_user, fresh=False)
        jti = get_jwt.add()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token" : new_token}, 200


@blp.route("/user")
class User(MethodView):

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(cls):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)
        return user

    @jwt_required(refresh=True)
    @blp.arguments(UserUpdateSchema)
    @blp.response(201, UserSchema)
    def put(cls, user_data):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)

        if 'name' in user_data:
            user.name = user_data["name"]

        if 'username' in user_data:
            if UserModel.filter(UserModel.username == user_data["username"], UserModel.id != user_id, with_deleted=True).first():
                abort(409, message="username token, try again!")
            else:
                user.username = user_data["username"]
            
        if 'email' in user_data:
            if UserModel.filter(UserModel.email == user_data["email"], UserModel.id != user_id, with_deleted=True).first():
                abort(409, message="email belong to another account!")
            else:
                user.email = user_data["email"]
                
        user.updated = datetime.now()

        try:
            db.session.add(user)
            db.session.commit()
            return user

        except Exception as e:
            abort(500, message=f"error => {e} !")


    @jwt_required(refresh=True)
    def delete(self):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)
        username = user.username
        try:
            UserModel.soft_delete(user)
            return {"message": f"user {username} deleted successfully"}
        
        except Exception as e:
            abort(500, message=f"error => {e} !")

@blp.route("/user/password")
class UserPassword(MethodView):
    @jwt_required(refresh=True)
    @blp.arguments(PassUpdateSchema)
    def post(self, pass_data):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)
        if pbkdf2_sha256.verify(pass_data["old_password"], user.password):
            new_password = pbkdf2_sha256.hash(str(pass_data["new_password"]))

            try:
                user.password = new_password
                user.updated = datetime.now()
                db.session.add(user)
                db.session.commit()
                return {"message" : "password update successfully !"}, 201
            
            except Exception as e:
                abort(500, message=f"error => {e} !")
        
        else:
            abort(409, message="password incorrect!")

    
