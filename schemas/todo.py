from marshmallow import fields, Schema
from schemas.base_schema import BaseSchema


class PlainListSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    color = fields.String()
    is_active = fields.Boolean(required=True)


class PlainTaskSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    due_date = fields.Date()
    priority = fields.Int()
    is_completed = fields.Boolean()
    category = fields.Str()


class ListSchema(PlainListSchema):
    user_id = fields.Int()
    tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)


class TaskSchema(PlainTaskSchema):
    list_id = fields.Int(load_only=True)

    list = fields.Nested(PlainListSchema(), dump_only=True)

class UpdateTaskSchema(Schema):
    list_id = fields.Int()
    name = fields.String()
    description = fields.String()
    due_date = fields.DateTime()
    priority = fields.Int()
    is_completed = fields.Boolean()
    category = fields.Str()


class UpdateListSchema(Schema):
    name = fields.String()
    color = fields.String()
    is_active = fields.Boolean()