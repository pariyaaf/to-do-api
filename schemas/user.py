from marshmallow import Schema, fields
from schemas.base_schema import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=False)
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    is_admin = fields.Boolean(required=False)


class UserUpdateSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    username = fields.Str()

class PaaUpdateSchema(Schema):
    new_password = fields.Str(required=True)
    old_password = fields.Str(required=True)