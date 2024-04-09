from marshmallow import Schema, fields, validate, validates, ValidationError

# from marshmallow_enum import EnumField


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)  # dump_only means it won't be deserialized
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True, validate=validate.Length(min=5, max=50))
    first_name = fields.String(validate=validate.Length(min=3, max=50))
    last_name = fields.String(validate=validate.Length(min=3, max=50))
    date_of_birth = fields.Date()
    password = fields.String(
        load_only=True, required=True, validate=validate.Length(min=8)
    )
    bio = fields.String()
    profile_picture = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    password = fields.String(required=True, validate=validate.Length(min=8))


class UserQuerySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.String(dump_only=True)
    question = fields.String()
    answer = fields.String()
    created_at = fields.DateTime(dump_only=True)
