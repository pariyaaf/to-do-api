from flask.views import MethodView
from flask_smorest import Blueprint, abort, current_api
from schemas.user import UserSchema, UserUpdateSchema
from models import UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity, create_refresh_token
from datetime import datetime
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(cls, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.arguments(UserUpdateSchema)
    @blp.response(201, UserSchema)
    def put(cls, user_id):
        pass



@blp.route("/user/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    # @blp.response(201, UserSchema)
    def post(cls, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
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
            abort(500, message="An erro occurred while inserting the new data!")

        except:
            abort(520, message="error!")

        return {"message": "user created successfully"}, 201  



@blp.route("/user/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    def post(cls, user_data):
        user = UserModel.query.filter(user_data["username"] == UserModel.username).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token" : access_token, "refresh_token" : refresh_token}

        abort(401, message="invalid data")



@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
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


@blp.route("/users")
class Admin(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(cls):
        users = UserModel.query.all()
        return users