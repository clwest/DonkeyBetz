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


# Generate slug for blog titles
def generate_slug(title):
    # convert to lower case
    slug = title.lower()
    # replace spaces and underscores with hyphes
    slug = re.sub(r'[\s_]+', '-', slug)
    # remove all characters that are not alphanumeric or hyphens
    slug = re.sub(r'[^\w-]', '', slug)
    # remove leading and trailing hyphens
    slug = slug.strip('-')

    return slug

def generate_unique_slug(title):
    base_slug = generate_slug(title)
    unique_slug = base_slug
    counter = 1
    while slug_exists(unique_slug):
        unique_slug = f"{base_slug}-{counter}"
        counter +=1
    return unique_slug

def slug_exists(model, slug):
    try:
        # check if any instance exists in the database with the given slug
        exists = model.query.filter_by(slug=slug) is not None
        return exists
    except Exception as e:
        logger.error(f"An error occurred while checking slug existence: {e}")
        raise InternalServerError("An error occurred while checking slug existence.")