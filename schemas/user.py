from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=False)
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    is_admin = fields.Boolean(required=False)


class UserUpdateSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    username = fields.Str()
    password = fields.Str()
    is_admin = fields.Boolean()