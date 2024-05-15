import uuid
from datetime import datetime
import logging
import os
from typing import Any
from enum import Enum
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
    Table,
    JSON,
    UUID
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, Enum as SQLAlchemyEnum
from pgvector.sqlalchemy import Vector
from factory import db
import helpers.helper_functions as hf

from models.shared_tables import chatbot_interactions_table, user_agent_table, user_project_table
from models.blogs import Post
from models.chatbots import Chatbot
from models.crews import Agent


class DocumentType(Enum):
    URL = "url"
    PDF = "pdf"
    VIDEO = "video"
    GITHUB = "github"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(String(50), index=True, nullable=True)
    last_name = db.Column(String(50), index=True, nullable=True)
    date_of_birth = db.Column(DateTime(timezone=True), nullable=True)
    email = db.Column(String(100), unique=True, nullable=False, index=True)
    password = db.Column(String(256), nullable=False)
    bio = db.Column(Text, nullable=True)
    profile_picture = db.Column(String(50), nullable=True)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now())

    # Relationships

    agents = relationship(
        "Agent",
        secondary=user_agent_table,
        back_populates="user",
    )

    posts = relationship(
        "Post", back_populates="user", cascade="all, delete-orphan", lazy=True
    )

    projects = relationship(
        "Project",
        secondary=user_project_table,
        back_populates="users"
    )

    chatbots = relationship(
        "Chatbot",
        secondary=chatbot_interactions_table,
        back_populates="users",
    )
    crews = relationship("Crew", back_populates="user")

    user_queries = relationship(
        "UserQuery", back_populates="user", cascade="all, delete-orphan"
    )
    conversation_sessions = relationship(
        "ConversationSession", back_populates="user", cascade="all, delete-orphan"
    )

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_learning_process(self, new_process):
        self.learning_process = new_process
        hf.update_db()

    def update_preferences(self, new_preferences):
        self.preferences = new_preferences
        hf.update_db()

    def __repr__(self):
        return f"<User {self.username}>"
    
    __table_args__ = (
        db.Index("idx_username_email", "username", "email", "created_at"),
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.password = generate_password_hash(kwargs['password'], method='scrypt')

    def __repr__(self):
        return f'<User {self.username}>'



class BlacklistedToken(db.Model):
    id = db.Column(Integer, primary_key=True)
    token = db.Column(String(256), unique=True, nullable=False, index=True)
    blacklisted_on = db.Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<BlacklistedToken {self.token}>"


class UserQuery(db.Model):
    __tablename__ = "user_query"
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(String(36), ForeignKey("users.id"), index=True)
    question = db.Column(Text, nullable=False)
    answer = db.Column(Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="user_queries")

    def __repr__(self):
        return f"<UserQuery {self.id}>"

    __table_args__ = (
        db.Index(
            "idx_user_id_created_at",
            "user_id",
            "created_at",
        ),
    )


class CollectionStore(db.Model):
    __tablename__ = "langchain_pg_collection"

    uuid = db.Column(db.UUID(as_uuid=True), primary_key=True)
    name = db.Column(String)
    cmetadata = db.Column(JSON)
    project_id = db.Column(Integer, ForeignKey("projects.id"))

    # Relationships
    embeddings = db.relationship('EmbeddingStore', back_populates="collection", passive_deletes=True)
    project = db.relationship('Project', back_populates='collections')


class EmbeddingStore(db.Model):
    __tablename__ = "langchain_pg_embedding"

    uuid = db.Column(db.UUID(as_uuid=True), primary_key=True)
    collection_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('langchain_pg_collection.uuid', ondelete='CASCADE'), nullable=False)
    embedding = db.Column(Vector(1536)) 
    document = db.Column(String)
    cmetadata = db.Column(JSON)
    custom_id = db.Column(String)

    collection = db.relationship('CollectionStore', back_populates="embeddings")


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(255))
    collection_name = db.Column(String(80), unique=True, nullable=False)
    source_type = db.Column(SQLAlchemyEnum(DocumentType), index=True)
    content = db.Column(Text)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", secondary=user_project_table, back_populates="projects")
    collections = db.relationship('CollectionStore', back_populates='project')