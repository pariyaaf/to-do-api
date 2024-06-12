from flask import request 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.todo import ListSchema, UpdateListSchema
from models import ListModel, UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from public_methods import str_to_bool


blp = Blueprint("Lists", "lists", description="Operations on lists")

@blp.route("/user/list")
class List(MethodView):
    @jwt_required(refresh=True)
    @blp.arguments(ListSchema)
    @blp.response(200, ListSchema)
    def post(self, list_data):
        user = UserModel.get(get_jwt_identity())

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
        user_id = get_jwt_identity()
        print(user_id)
        user = UserModel.get_or_404(user_id)
        try:

            param_1 = request.args.get('with_deleted', 'false')
            with_deleted = str_to_bool(param_1)
            lists = ListModel.filter_by(user_id=user.id, with_deleted=with_deleted).all()
            return lists
        
        except Exception as e:
            abort(500, message=f"error => {e} !")



@blp.route("/user/list/<int:list_id>")
class ListId(MethodView):

    @jwt_required()
    @blp.response(200, ListSchema())
    def get(self, list_id):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)

        param_1 = request.args.get('with_deleted', 'false')
        with_deleted = str_to_bool(param_1)
        try:
            list = ListModel.filter_by(user_id=user.id, id=list_id, with_deleted=with_deleted).first()
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
        user = UserModel.get_or_404(user_id)
        list = ListModel.filter_by(user_id=user.id).filter_by(id=list_id).first()
        
        if not list:
            abort(404, message="List not found!")

        try:
            if 'name' in list_data:
                list.name = list_data["name"]
            if 'color' in list_data:
                list.color = list_data["color"]
            if 'is_active' in list_data:
                list.is_active = list_data["is_active"]

            ListModel.update_record(list, user_id)
            return list
        except Exception as e:
            abort(500, message=f"error happen please try again! \n {e}")


    @jwt_required(refresh=True)
    def delete(self, list_id):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)
        list = ListModel.get_or_404(list_id)

        if list.is_active:
            abort(400, message="list is active!")

        try:
            ListModel.soft_delete(list, user_id)

            return {"message": "list deleted"}
            
        except Exception as e:
            abort(500, message=f"error => {e} !")

