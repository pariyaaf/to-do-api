from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.todo import ListSchema, UpdateListSchema
from models import ListModel, UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime


blp = Blueprint("Lists", "lists", description="Operations on lists")

@blp.route("/user/list")
class List(MethodView):
    @jwt_required(refresh=True)
    @blp.arguments(ListSchema)
    @blp.response(200, ListSchema)
    def post(self, list_data):
        user = UserModel.query.get(get_jwt_identity())

        if user is None:
            abort(404, message="user id not found!")

        list =  ListModel(
            name = list_data["name"],
            color =   list_data["color"] if "color" in list_data else "blue",
            is_active = bool(list_data["is_active"]),
            user_id = user.id,
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow(),
        )
        try:
            db.session.add(list)
            db.session.commit()
        
        except IntegrityError:
            abort(400, message="list already exists")

        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting  the new list")

        return list 
    
    @jwt_required()
    @blp.response(200, ListSchema(many=True))
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = UserModel.query.get_or_404(user_id)
            lists = ListModel.query.filter_by(user_id=user.id).all()
            return lists
        
        except Exception as e:
            abort(500, message=f"error => {e} !")




@blp.route("/user/list/<int:list_id>")
class ListId(MethodView):

    @jwt_required()
    @blp.response(200, ListSchema())
    def get(self, list_id):
        try:
            user_id = get_jwt_identity()
            user = UserModel.query.get_or_404(user_id)
            list = ListModel.query.filter_by(user_id=user.id).filter_by(id=list_id).first()
            
            if not list:
                abort(404, message="List not found!")
            
            return list

        except Exception as e:
            abort(500, message=f"error => {e} !")



    @jwt_required(refresh=True)
    @blp.arguments(UpdateListSchema())
    @blp.response(201, ListSchema())
    def put(self, list_data, list_id):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        list = ListModel.query.filter_by(user_id=user.id).filter_by(id=list_id).first()
        
        if not list:
            abort(404, message="List not found!")

        try:
            if 'name' in list_data:
                list.name = list_data["name"]
            if 'color' in list_data:
                list.color = list_data["color"]
            if 'is_active' in list_data:
                list.is_active = list_data["is_active"]

            list.updated_at =  datetime.utcnow()

            db.session.add(list)
            db.session.commit()

            return list
        except Exception as e:
            abort(500, message=f"error happend please try egain! \n {e}")


    @jwt_required(refresh=True)
    def delete(self, list_id):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        list = ListModel.query.get_or_404(list_id)

        if list.is_active:
            abort(400, message="list is active!")

        try:
            db.session.delete(list)
            db.session.commit()
            return {"message": "list deleted"}
            
        except Exception as e:
            abort(500, message=f"error => {e} !")

