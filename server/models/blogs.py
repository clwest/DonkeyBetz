from datetime import datetime
import re
import os
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
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.sql import func
from sqlalchemy import Column, Enum as SQLAlchemyEnum
from factory import db
import helpers.helper_functions as hf

# from langchain_utils.agents import content_creator
from models.shared_tables import post_categories_table, post_tags_table


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(String(100), nullable=False)
    slug = db.Column(String(250), nullable=False, unique=True, index=True)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    is_draft = db.Column(Boolean, default=True, index=True)
    view_count = db.Column(Integer, default=0)
    date_posted = db.Column(DateTime, default=datetime.utcnow)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user_id = db.Column(String(36), ForeignKey("users.id"), index=True)

    user = relationship("User", back_populates="posts")
    # Placeholders for categories and tags
    categories = relationship(
        "Category",
        secondary=post_categories_table,
        back_populates="posts",
    )
    tags = relationship(
        "Tag",
        secondary=post_tags_table,
        back_populates="posts",
    )
 
    def generate_slug(self):
        # Method to generate a unique slug for a post
        slug = self.title.lower()
        # Replace non-word characters
        slug = re.sub(r"\W+", "-", slug)

        # Check for uniqueness
        original_slug = slug
        counter = 1
        while True:
            existing_post = Post.query.filter_by(slug=original_slug).first()
            if not existing_post:
                break
            slug = f"{original_slug}-{counter}"
            counter += 1

        self.slug = slug


    def update_view_count(self):
        self.view_count += 1
        hf.update_db()

    def ai_enhance(self):
        pass

    # def langchain_assist(self):
    #     try:
    #         enhanced_content = content_creator(self.content)
    #         self.content = enhanced_content
    #         hf.update_db()
    #     except Exception as e:
    #         print(f"Error using Langchain assist: {e}")

    __table_args__ = (
        db.Index(
            "idx_post_title_user",
            "title",
            "user_id",
            "date_posted",
        ),
    )

    def __repr__(self):
        return f"<Post {self.title}>"


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True, nullable=False, index=True)
    posts = relationship(
        "Post",
        secondary=post_tags_table,
        back_populates="tags",
    )

    __table_args__ = (
        db.Index(
            "idx_tag_name",
            "name",
        ),
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True, nullable=False, index=True)
    posts = relationship(
        "Post",
        secondary=post_categories_table,
        back_populates="categories",
    )

    __table_args__ = (
        db.Index(
            "idx_category_name",
            "name",
        ),
    )

    def __repr__(self):
        return f"<Category {self.name}>"
