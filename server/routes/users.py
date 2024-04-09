import re
import logging
import uuid
import os
from pprint import pprint
from datetime import datetime, timedelta
from dotenv import load_dotenv
import spacy

# Flask configuration
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import request, jsonify, make_response
# from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Helpers and other functions
from factory.limiter_factory import limiter
from factory import db
from helpers.constants import *
from helpers.helper_permissions import *
from models.users import User, UserQuery
from utils.content_utils import *
from schemas.users import *
from services.auth import check_if_token_in_blacklist
from services.logging_config import root_logger as logger
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf

load_dotenv()


# Function to register a new user
users_blp = Blueprint("users", "users", url_prefix="/api/users")
user_schema = UserSchema()
user_login_schema = UserLoginSchema()

nlp = spacy.load("en_core_web_sm")


@users_blp.route("/register", methods=["POST"])
class RegisterAPI(MethodView):
    # @users_blp.arguments(UserSchema)
    @users_blp.response(201, description="User registered successfully")
    def post(self):
        data = request.json
        logger.info(f"Printing the data: {data}")
        validated_data, error = hf.validate_data(user_schema, data)

        if error:
            logger.error(f"Validation error: {error}")
            raise ce.BadRequestError("Invalid request", error)
        logger.info(f"Validation successful. Validated data: {validated_data}")

        new_user = User(
            **validated_data,
        )
        logger.info(f"Printing the new user: {new_user}")
        hf.add_to_db(new_user)
        logger.info(f"User added to db: {new_user}")

        # generate access token
        access_token = create_access_token(
            identity={"id": new_user.id, "username": new_user.username}
        )

        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "access_token": access_token,
                }
            ),
            201,
        )


# Function to login a user
@users_blp.route("/login", methods=["POST"])
class LoginAPI(MethodView):
    def post(self):
        data = request.json
        logger.info(f"Printing the data: {data}")

        validated_data, error = hf.validate_data(user_login_schema, data)
        if error:
            logger.error(f"Validation error: {error}")
            raise ce.BadRequestError("Invalid request", error)
        logger.info(f"Validation successful. Validated data: {validated_data}")

        username = validated_data.get("username")
        password = validated_data.get("password")

        # Fetch user by username
        user = User.query.filter_by(username=username).first()
        if user:
            logger.info(f"User found: {username}")
        else:
            logger.error(f"User not found: {username}")
            raise ce.UserNotFoundError("User not found", 404)
        

        # Check password
        logger.info(f"Attempting to validate password for user: {username}")
        if not user.check_password(password):
            logger.error(f"Invalid credentials for user: {username}")
            raise  ce.InvalidCredentialsError("Invalid credentials", 401)
            

        user_data = {"id": user.id, "username": user.username, "email": user.email, "bio": user.bio}
        
        logger.info(f"Login successful for user: {username}. Generating access token...")
        # Generate access token
        access_token = create_access_token(
            identity={"id": user.id, "username": user.username, "email": user.email}
        )
        refresh_token = create_refresh_token(
            identity={"id": user.id, "username": user.username, "email": user.email}
        )
        response = make_response(
            jsonify({"message": "Logged in", "access_token": access_token})
        )
        response.set_cookie("access_token", access_token, httponly=True)

        logger.info(f"Printing the response: {response}")
        return (
            jsonify(
                {
                    "message": "Logged in",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_data,
                }
            ),
            200,
        )


@users_blp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    if not user:
        raise ce.UserNotFoundError("User not found", 404)
    access_token = create_access_token(
        identity={"id": user.id, "username": user.username}
    )
    return jsonify(access_token=access_token)


# Function to logout a user
@users_blp.route("/logout", methods=["POST"])
class LogoutAPI(MethodView):
    @set_current_user
    def post(self):
        jti = get_jwt()["jti"]

        try:
            check_if_token_in_blacklist(jti)
            response = make_response(jsonify({"message": "Logged out"}))
            response.set_cookie("access_token", "", httponly=True, expires=0)
            return jsonify({"message": "Logged out"}), 200
        except ce.TokenBlacklistError:
            return jsonify({"message": "Something went wrong"}), 500
        except Exception as e:
            logging.error(f"Failed to logout user: {e}")
            return jsonify({"message": "Something went wrong"}), 500



