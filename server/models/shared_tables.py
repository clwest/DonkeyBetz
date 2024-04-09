from sqlalchemy import Table, ForeignKey, Integer, String
from factory import db


agent_crew_mapping = Table(
    "agent_crew_mapping",
    db.metadata,
    db.Column("agent_id", Integer, ForeignKey("agents.id"), primary_key=True),
    db.Column("crew_id", Integer, ForeignKey("crews.id"), primary_key=True),
)


agent_task_table = Table(
    "agent_tasks_table",
    db.metadata,
    db.Column("agent_id", Integer, ForeignKey("agents.id"), primary_key=True),
    db.Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
)

chatbot_interactions_table = Table(
    "chatbot_interactions_table",
    db.metadata,
    db.Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    db.Column("chatbot_id", Integer, ForeignKey("chatbots.id"), primary_key=True),
)

user_agent_table = Table(
    "user_agent_table",
    db.metadata,
    db.Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    db.Column("agent_id", Integer, ForeignKey("agents.id"), primary_key=True),
)

post_tags_table = Table(
    "post_tags_table",
    db.metadata,
    db.Column("post_id", Integer, ForeignKey("posts.id")),
    db.Column("tag_id", Integer, ForeignKey("tags.id")),
)

post_categories_table = Table(
    "post_categories_table",
    db.metadata,
    db.Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    db.Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)

agent_chatbot_table = Table(
    "agent_chatbot_table",
    db.metadata,
    db.Column("agent_id", Integer, ForeignKey("agents.id"), primary_key=True),
    db.Column("chatbot_id", Integer, ForeignKey("chatbots.id"), primary_key=True),
)

chatbot_tool_link = Table(
    "chatbot_tool_link",
    db.metadata,
    db.Column("tool_id", Integer, ForeignKey("tools.id"), primary_key=True),
    db.Column("chatbot_preferences_id", Integer, ForeignKey("chatbot_preferences.id"), primary_key=True),
)


user_project_table = Table(
    "user_projects_table",
    db.metadata,
    db.Column("user_id", String(36), ForeignKey('users.id')),
    db.Column("project_id", Integer, ForeignKey('projects.id'))
)