# from marshmallow import Schema, fields, validate, validates, ValidationError
# from marshmallow_enum import EnumField


# class BlockchainSchema(Schema):
#     id = fields.Str()
#     name = fields.Str()
#     description = fields.Str()
#     documentation_url = fields.Url()
#     whitepaper_url = fields.Url()
#     category = fields.Str()
#     created_at = fields.DateTime()
#     updated_at = fields.DateTime()


# class BlockchainVectorSchema(Schema):
#     id = fields.Int()
#     blockchain_id = fields.Str()
#     embedding = fields.List(fields.Float(), validate=lambda x: len(x) == 1536)
#     blockchain_metadata = fields.Dict()
#     tags = fields.Str()
#     description = fields.Str()
