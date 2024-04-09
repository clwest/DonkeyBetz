# Description: Chatbot models for the application
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
    JSON,
)

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, Enum as SQLAlchemyEnum
from factory import db
import helpers.helper_functions as hf

from models.shared_tables import (
    agent_chatbot_table,
    chatbot_interactions_table,
    chatbot_tool_link,
)
from models.crews import Agent


class MessageType(Enum):
    USER = "user"
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"


class ConversationStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"
    ENDED = "ended"
    


class Chatbot(db.Model):
    __tablename__ = "chatbots"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, index=True, unique=True)
    description = db.Column(Text, nullable=True)
    user_id = db.Column(String(36), ForeignKey("users.id"), index=True)
    # Collection Name from PGVector
    collection_name = db.Column(UUID(as_uuid=True), nullable=True, index=True)  
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    conversation_sessions = relationship(
        "ConversationSession", back_populates="chatbot"
    )
    agents = relationship(
        "Agent", secondary=agent_chatbot_table, back_populates="chatbot"
    )
    users = relationship(
        "User", secondary=chatbot_interactions_table, back_populates="chatbots"
    )

    preferences = relationship("ChatbotPreference", back_populates="chatbot")

    __table_args__ = (
        db.Index(
            "idx_name_user_topic_collection",
            "name",
            "user_id",
            "collection_name",
            "created_at",
        ),
    )

    def __repr__(self):
        return f"<Chatbot {self.id}>"
    



class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(Integer, primary_key=True)
    session_id = db.Column(String(36), ForeignKey("conversation_session.id"), nullable=False, index=True)
    sender_id = db.Column(Text, index=True) # E.g., 'user id', 'bot', 'agent'
    message_type = db.Column(Text)  # E.g., 'user', 'bot', 'agent'
    content = db.Column(Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationship to ConversationSession
    session = relationship('ConversationSession', back_populates='messages')

    __table_args__ = (
        db.Index(
            "idx_session_sender_type",
            "session_id",
            "sender_id",
            "message_type",
            "created_at",
        ),
    )


    def __repr__(self):
        return f"<ChatMessage {self.id}>"
    

class ConversationSession(db.Model):
    __tablename__ = "conversation_session"
    id = db.Column(String(36), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(String(36), ForeignKey("users.id"), index=True)
    chatbot_id = db.Column(Integer, ForeignKey("chatbots.id"), index=True)
    topic_name = db.Column(String(250), index=True)
    description = db.Column(String(250))
    session_metadata = db.Column(JSON, nullable=True)
    conversation_status = db.Column(SQLAlchemyEnum(ConversationStatus), index=True)
    last_accessed = db.Column(DateTime(timezone=True), onupdate=func.now(), index=True)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    ended_at = db.Column(DateTime(timezone=True), default=func.now())

    user = relationship("User", back_populates="conversation_sessions")
    chatbot = relationship("Chatbot", back_populates="conversation_sessions")
    messages = relationship('ChatMessage', order_by=ChatMessage.id, back_populates='session')

    __table_args__ = (
        db.Index(
            "idx_user_topic_status",
            "user_id",
            "topic_name",
            "conversation_status",
            "last_accessed",
        ),
    )
    
    def __repr__(self):
        return f"<ConversationSession {self.id}>"

class ChatbotSettings(db.Model):
    __tablename__ = "chatbot_settings"
    id = db.Column(Integer, primary_key=True)
    personality_type = db.Column(
        String(50), index=True
    )  # Casual, Formal, Humorous, Proactive, Reactive
    interaction_mode = db.Column(String, index=True)  # text-only, voice-enabled
    voice_type = db.Column(String(10), index=True)  # male, female, custom
    # Researching more to add

    # Relationship
    chatbot_id = db.Column(Integer, ForeignKey("chatbots.id"), index=True)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    __table_args__ = (
        db.Index(
            "idx_personality_interaction_voice",
            "personality_type",
            "interaction_mode",
            "voice_type",
            "created_at",
        ),
    )
    
    def __repr__(self):
        return f"<ChatbotSettings {self.id}>"


class ChatbotPreference(db.Model):
    __tablename__ = "chatbot_preferences"
    id = db.Column(Integer, primary_key=True)
    topic_types = db.Column(
        String, index=True
    )  # Investment, Research, Sports, Entertainment, etc.
    content_sources = db.Column(String, index=True)  # APIs Yahoo, Sports, News ETC
    chatbot_id = db.Column(
        Integer, ForeignKey("chatbots.id"), index=True, nullable=False
    )
    tool_preferences = db.Column(ARRAY(Integer))

    # Relationships
    tools = relationship("Tool", secondary=chatbot_tool_link, back_populates="preferences")
    chatbot = relationship("Chatbot", back_populates="preferences")
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


    def __repr__(self):
        return f"<ChatbotPreference {self.id}>"


class Tool(db.Model):
    __tablename__ = "tools"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)
    description = db.Column(Text)
    configuration = db.Column(JSON)  # or Text, if storing as XML
    is_active = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationship
    preferences = relationship(
        "ChatbotPreference", secondary=chatbot_tool_link, back_populates="tools"
    )
    
    def __repr__(self):
        return f"<Tool {self.id}>"


