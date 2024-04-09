from marshmallow import Schema, fields, validate, validates, ValidationError
from schemas.users import UserSchema
from schemas.crews import AgentSchema
from models.chatbots import ConversationStatus, MessageType


class ChatbotSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=3, max=50))
    user_id = fields.String()
    description = fields.String()
    collection_name = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    user = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)
    session = fields.Nested("ConversationSessionSchema", only=("id", "session_metadata"), dump_only=True)
    agents = fields.Nested(AgentSchema, dump_only=True)
    preferences = fields.Nested("ChatbotPreferenceSchema", dump_only=TabError)

class ChatMessageSchema(Schema):
    id = fields.Int(dump_only=True)
    session_id = fields.String()
    sender_id = fields.String()
    message_type = fields.String()
    content = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ConversationSessionSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String()
    chatbot_id = fields.Int()
    topic_name = fields.String(required=True, validate=validate.Length(min=5, max=25))
    description = fields.String()
    session_metadata = fields.String()
    conversation_status = fields.Method(
        serialize="serialize_status", deserialize="deserialize_status"
    )
    last_accessed = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    ended_at = fields.DateTime()

    user = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)
    chatbot = fields.Nested(ChatbotSchema, only=("id", "name"), dump_only=True)
    messages = fields.Nested(ChatMessageSchema, only=("id", "sender_id", "message_type", "content")) 

    def serialize_status(self, obj):
        return obj.conversation_status.name if obj.conversation_status else None

    def deserialize_status(self, value):
        if value in ConversationStatus._member_names_:
            return ConversationStatus[value]
        raise ValidationError("Invalid status")


class ChatbotSettingsSchema(Schema):
    id = fields.Int(dump_only=True)
    personality_type = fields.String()
    interaction_mode = fields.String()
    voice_type = fields.String()


    chatbot = fields.Nested(ChatbotSchema, only=("id", "name"))


class ChatbotPreferenceSchema(Schema):
    id = fields.Int(dump_only=True)
    topic_types = fields.String()
    content_sources = fields.String()


    chatbot = fields.Nested(ChatbotSchema, only=("id", "name"))


class ToolSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    description = fields.String()

    chatbot = fields.Nested(ChatbotSchema, only=("id", "name"))

