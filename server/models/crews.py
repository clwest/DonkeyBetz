from datetime import datetime
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

from models.shared_tables import (
    agent_chatbot_table,
    user_agent_table,
    agent_task_table,
    agent_crew_mapping,
)

# from models.users import User
# from models.chatbots import Chatbot


class Agent(db.Model):
    __tablename__ = "agents"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(30), index=True)
    role = db.Column(String(30), index=True)
    goal = db.Column(String(500))
    backstory = db.Column(String(500))
    user_id = db.Column(String(36), ForeignKey("users.id"), index=True)
    created_at = db.Column(DateTime, default=func.now())
    updated_at = db.Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship(
        "User",
        secondary=user_agent_table,
        back_populates="agents",
    )
    tasks = relationship(
        "Task",
        secondary=agent_task_table,
        back_populates="agents",
    )
    crews = relationship(
        "Crew",
        secondary=agent_crew_mapping,
        back_populates="agents",
    )
    chatbot = relationship(
        "Chatbot",
        secondary=agent_chatbot_table,
        back_populates="agents",
    )

    __table_args__ = (
        db.Index(
            "idx_agent_name_user_role",
            "name",
            "user_id",
            "role",
            "created_at"
        ),
    ) # Index for agent name.\n

    def __repr__(self):
        return f"<Agent {self.name}>"


class Crew(db.Model):
    __tablename__ = "crews"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(40), index=True)
    result_content = db.Column(Text)
    user_id = db.Column(String(36), ForeignKey("users.id"), index=True)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="crews")
    agents = relationship("Agent", secondary=agent_crew_mapping, back_populates="crews")

    __table_args__ = (
        db.Index(
            "idx_crew_name_user",
            "name",
            "user_id",
            "created_at"
        ),
    ) # Index for crew name.\n

    def __repr__(self):
        return f"<Crew {self.name}>"


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(Integer, primary_key=True)
    description = db.Column(Text)
    status = db.Column(String(50))
    agent_id = db.Column(Integer, ForeignKey("agents.id"), index=True)
    crew_id = db.Column(Integer, ForeignKey("crews.id"), index=True)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    agents = relationship(
        "Agent",
        back_populates="tasks",
        secondary=agent_task_table,
    )
    result = relationship("TaskResult", uselist=False, back_populates="task")

    __table_args__ = (
        db.Index(
            "idx_task_description_status_agent_crew",
            "description",
            "status",
            "agent_id",
            "crew_id",
            "created_at"
        ),
    ) # Index for task description.\n

    def __repr__(self):
        return f"<Task {self.id}>"

class TaskResult(db.Model):
    __tablename__ = "task_results"
    id = db.Column(Integer, primary_key=True)
    task_id = db.Column(Integer, ForeignKey("tasks.id"), index=True)
    result_content = db.Column(Text)
    created_at = db.Column(DateTime(timezone=True), default=func.now())
    updated_at = db.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    task = relationship("Task", back_populates="result")

    __table_args__ = (
        db.Index(
            "idx_task_result_task_id",
            "task_id",
            "created_at"
        ),
    ) # Index for task result.\n

    def __repr__(self):
        return f"<TaskResult {self.id}>"
