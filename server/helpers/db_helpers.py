from pprint import pprint
import os
from dotenv import load_dotenv
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf
from factory import create_app, db
from models.users import User, Role, Permission


def initialize_database():
    """Initialize the database."""
    app = create_app()
    with app.app_context():
        db.create_all()


def seed_roles_and_permissions():
    app = create_app()
    with app.app_context():
        # Create roles
        admin_role = Role(name="Admin")
        creator_role = Role(name="Creator")
        user_role = Role(name="User")

        # Create permissions
        create_content = Permission(name="Create Content")
        edit_content = Permission(name="Edit Content")
        delete_content = Permission(name="Delete Content")

        # Assign permissions to roles
        creator_role.permissions.extend([create_content, edit_content, delete_content])

        # Add roles and permissions to the session and commit
        hf.add_to_db(
            [
                admin_role,
                creator_role,
                user_role,
                create_content,
                edit_content,
                delete_content,
            ]
        )


def add_user(username, email, password):
    """Add a new user to the database."""
    app = create_app()
    with app.app_context():
        new_user = User(username=username, email=email, password=password)
        hf.add_to_db(new_user)
