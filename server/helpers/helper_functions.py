import re
from contextlib import contextmanager
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import text
from .custom_exceptions import *
from .helper_permissions import *
from services.logging_config import root_logger as logger


# Data Validation using Marshmallow
def validate_data(schema, data):
    try:
        return schema.load(data), None
    except ValidationError as e:
        return None, jsonify({"message": str(e)}), 400

# Validate the request data
def validate_user_details(email, username, password):
    if not validate_email(email):
        raise ValidationError("Invalid email format")
    if len(password) < 8 or not re.search('[a-zA-Z0-9!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Weak Password")
    if len(username) < 3 or not re.match("^[a-zA-Z0-9_]+$", username):
        raise ValidationError("Invalid username")
    return None

# Check if the email is valid
def check_existing_user(email, username):
    from backend.models.users import User

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        raise UserAlreadyExistsError("Email already registered")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise UserAlreadyExistsError("Username already exists")
    return None


@contextmanager
# Create a session scope
def session_scope():
    from factory import db

    """Provide a transactional scope around a series of operations."""
    try:
        yield db.session
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"An error occurred: {e}")
        raise
    finally:
        pass

# Add an instance to the database
def add_to_db(instance):
    with session_scope() as session:
        try:
            session.add(instance)
            session.commit()
            instance_id = instance.id
        except IntegrityError:
            raise DataValidationError("Data integrity violation.")
        except InvalidRequestError:
            raise BadRequestError("Invalid request for database.")
        except Exception as e:
            logger.error(
                f"An error occurred while adding the resource to the database: {e}"
            )
            raise InternalServerError(
                "An error occurred while adding the resource to the database."
            )
    return instance_id

# Delete an instance from the database
def delete_from_db(instance):
    with session_scope() as session:
        try:
            session.delete(instance)
        except IntegrityError:
            raise DataValidationError(
                "Data integrity violation. Cannot delete the resource."
            )
        except InvalidRequestError:
            raise BadRequestError("Invalid request for database deletion.")
        except Exception as e:
            logger.error(
                f"An error occurred while deleting the resource from the database: {e}"
            )
            raise InternalServerError(
                "An error occurred while deleting the resource from the database."
            )

# Update the database
def update_db():
    from factory import db

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DataValidationError(
            "Data integrity violation. Cannot update the database."
        )
    except InvalidRequestError:
        db.session.rollback()
        raise BadRequestError("Invalid request for database update.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"An error occurred while updating the database: {e}")
        raise InternalServerError("An error occurred while updating the database.")

# Get single instance from the database
def get_db_object(model, **kwargs):
    """
    Fetch a single instance from the database based on the model and filter criteria.

    :param model: The SQLAlchemy model class to query.
    :param kwargs: Filter criteria passed to `filter_by`.
    :return: The first instance found or `None` if no instance matches the criteria.
    :raises: InternalServerError if an unexpected database error occurs.
    """
    try:
        return model.query.filter_by(**kwargs).first()
    except Exception as e:
        logger.error(f"An error occurred while getting the resource from the database: {e}")
        raise InternalServerError(
            "An error occurred while getting the resource from the database."
        )

# Get all instances from the database
def get_db_objects(model, **kwargs):
    """
    Fetch a all instances from the database based on the model and filter criteria.

    :param model: The SQLAlchemy model class to query.
    :param kwargs: Filter criteria passed to `filter_by`.
    :return: The all instances found or returns an empty list if no instance matches the criteria.
    :raises: InternalServerError if an unexpected database error occurs.
    """
    try:
        return model.query.filter_by(**kwargs).all()
    except Exception as e:
        logger.error(f"An error occurred while getting the resources from the database: {e}")
        raise InternalServerError(
            "An error occurred while getting the resources from the database."
        )
# Error Handling
def handle_error(message, status_code):
    return jsonify({"message": message}), status_code

def handle_db_error(e, operation_msg="performing operation"):
    """
    Handles database errors by logging and raising a standardized error.
    
    :param e: The exception object.
    :param operation_msg: A message describing the database operation being performed.
    :return: None
    :raises: A custom exception based on the error type.
    """
    logger.error(f"An error occurred while {operation_msg}: {e}")
    if isinstance(e, IntegrityError):
        raise DataValidationError("Data integrity violation.")
    elif isinstance(e, InvalidRequestError):
        raise BadRequestError("Invalid request for database operation.")
    else:
        raise InternalServerError("An unexpected error occurred in the database operation.")


# Check if an instance exists in the database
def instance_exists(model, **kwargs):
    return model.query.filter_by(**kwargs).first()


def enable_pgvector_extension():
    from factory import db

    """Enable the PGVector extension in the PostgreSQL database."""
    try:
        with db.engine.connect() as connection:
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        logger.info("PGVector extension enabled successfully.")
    except Exception as e:
        logger.error(f"Error enabling PGVector extension: {e}")
        raise


