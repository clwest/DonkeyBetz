from marshmallow import Schema, fields, validate, validates, ValidationError

from models.blogs import Tag, Category


class PostSchema(Schema):
    id = fields.Int(dump_only=True)  # dump_only means it won't be deserialized
    user_id = fields.Str()
    title = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    slug = fields.Str(dump_only=True) 
    content = fields.Str()
    summary = fields.Str()
    date_posted = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
    is_draft = fields.Boolean()
    view_count = fields.Int()
    

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # Nested schemao
    tags = fields.List(fields.Nested("TagSchema"), required=False)
    categories = fields.List(fields.Nested("CategorySchema"), required=False)

    # Method for the username
    username = fields.Method("get_username")

    def get_username(self, obj):
        return obj.user.username if obj.user else None


class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))

    @validates("name")
    def validate_name(self, value):
        if Tag.query.filter_by(name=value).first():
            raise ValidationError(f"Tag {value} already exists")


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))

    @validates("name")
    def validate_name(self, value):
        if Category.query.filter_by(name=value).first():
            raise ValidationError(f"Category {value} already exists")
