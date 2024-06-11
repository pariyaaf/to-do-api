from flask import request 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.todo import TaskSchema, UpdateTaskSchema
from models import TaskModel, UserModel, ListModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from public_methods import str_to_bool


blp = Blueprint("Tasks", "tasks", description="Operations on tasks")

@blp.route("/list/<int:list_id>/task")
class Task(MethodView):
    @jwt_required(refresh=True)
    @blp.arguments(TaskSchema)
    @blp.response(200, TaskSchema)
    def post(self, task_data, list_id):
        user = UserModel.get(get_jwt_identity())

        if user is None:
            abort(404, message="user not found!")

        existing_task = TaskModel.filter_by(
            list_id=list_id, name=task_data["name"]).first()
        
        if existing_task:
            abort(400, message="task with this name already exists")

        task = TaskModel(
            name=task_data["name"],
            description=task_data.get("description"),
            due_date=task_data.get("due_date", None),
            priority=int(task_data.get("priority", 1)),
            is_completed=bool(task_data.get("is_completed", False)),
            category=task_data.get("category", None),
            list_id=list_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        try:
            db.session.add(task)
            db.session.commit()
        
        except IntegrityError:
            abort(400, message="task already exists")

        except SQLAlchemyError as e:
            abort(500, message=f"error => {e} !")

        return task 
    
    @jwt_required()
    @blp.response(200, TaskSchema(many=True))
    def get(self, list_id):
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_or_404(user_id)
            param_1 = request.args.get('with_deleted', 'false')
            with_deleted = str_to_bool(param_1)
            tasks = TaskModel.filter_by(list_id=list_id, with_deleted=with_deleted).all()
            return tasks
        
        except Exception as e:
            abort(500, message=f"error => {e} !")



@blp.route("/list/<int:list_id>/task/<int:task_id>")
class TaskId(MethodView):

    @jwt_required()
    @blp.response(200, TaskSchema())
    def get(self, list_id, task_id):
        try:
            user_id = get_jwt_identity()
            user = UserModel.get_or_404(user_id)
            param_1 = request.args.get('with_deleted', 'false')
            with_deleted = str_to_bool(param_1)
            task = TaskModel.filter_by(list_id=list_id, id=task_id, with_deleted=with_deleted).first()
            
            if not task:
                abort(404, message="task not found!")
            return task
        
        except Exception as e:
            abort(500, message=f"error => {e} !")


    @jwt_required(refresh=True)
    @blp.arguments(UpdateTaskSchema())
    @blp.response(201, TaskSchema())
    def put(self, task_data, list_id, task_id):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)
        task = TaskModel.filter_by(list_id=list_id, id=task_id).first()
        
        if not task:
            abort(404, message="task not found!")

        try:
            if 'name' in task_data:
                task.name = task_data["name"]
            if 'description' in task_data:
                task.description = task_data["description"]
            if 'due_date' in task_data:
                task.due_date = task_data["due_date"]
            if 'priority' in task_data:
                    task.priority = task_data["priority"]
            if 'is_completed' in task_data:
                task.is_completed = task_data["is_completed"]
            if 'due_date' in task_data:
                task.due_date = task_data["due_date"]
            if 'category' in task_data:
                task.category = task_data["category"]
            if 'list_id' in task_data:
                task.list_id = task_data["list_id"]

            task.updated_at =  datetime.utcnow()

            db.session.add(task)
            db.session.commit()

            return task
        except Exception as e:
            abort(500, message=f"error => {e} !")


    @jwt_required(refresh=True)
    def delete(self, list_id, task_id):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)
        task = TaskModel.get_or_404(task_id)
        try:
            TaskModel.soft_delete(task)
            return {"message": "task deleted"}
            
        except Exception as e:
            abort(500, message=f"error => {e} !")



@blp.route('/user/tasks')
class UserTasks(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.get_or_404(user_id)
        try:
            list_ids_query = ListModel.filter_by(user_id=user_id).with_entities(ListModel.id).all()
            list_ids = [item.id for item in list_ids_query]
            param_1 = request.args.get('with_deleted', 'false')
            with_deleted = str_to_bool(param_1)
            tasks = TaskModel.filter(TaskModel.list_id.in_(list_ids, with_deleted=with_deleted)).all()
            return tasks
        except Exception as e:
            abort(500, message=f"error => {e} !")
