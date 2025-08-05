from marshmallow import Schema, fields

class BaseUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)

class UserCreateSchema(BaseUserSchema):
    password = fields.Str(required=True, load_only=True)

class UserUpdateSchema(BaseUserSchema):
    pass
