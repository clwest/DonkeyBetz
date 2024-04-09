from marshmallow import Schema, fields, validate, validates, ValidationError


from schemas.users import UserSchema


class AgentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=3, max=30))
    role = fields.String(required=True, validate=validate.Length(min=3, max=30))
    goal = fields.String()
    backstory = fields.String(required=True, validate=validate.Length(min=10, max=500))
    user_id = fields.String()

    user = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)


class CrewSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    result_content = fields.String()
    user_id = fields.String()

    user = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.String()
    status = fields.String()
    agent_id = fields.Int()
    crew_id = fields.Int()

    agent = fields.Nested(AgentSchema, only=("id", "name"), dump_only=True)
    crew = fields.Nested(CrewSchema, only=("id", "name"), dump_only=True)


class TaskResultSchema(Schema):
    id = fields.Int(dump_only=True)
    result_content = fields.String()
    task_id = fields.Int()
