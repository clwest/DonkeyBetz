
from flask import jsonify
import logging

import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger

def register_error_handlers(app):
  # Not Found Error
  @app.errorhandler(ce.NotFoundError)
  def handle_resource_not_found_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Not Found Error: {str(error)}")
      return jsonify({"message": str(error)}), error.status_code

  # Forbidden Error
  @app.errorhandler(ce.ForbiddenError)
  def handle_forbidden_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Forbidden Error: {str(error)}")
      return jsonify({"message": str(error)}), error.status_code

  # Validation Error
  @app.errorhandler(ce.ValidationError)
  def handle_validation_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Validation Error: {str(error)}")
      return jsonify({"message": error.message}), error.status_code


  # Rate Limit Exceeded
  @app.errorhandler(ce.RateLimitExceededError)
  def ratelimit_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Rate Limit Exceeded: {str(error)}")
      return jsonify({"message": str(error)}), error.status_code

  # Unauthorized Error
  @app.errorhandler(ce.UnauthorizedError)
  def handle_unauthorized_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Unauthorized Error: {str(error)}")
      return jsonify({"message": str(error)}), error.status_code

  # Internal Server Error
  @app.errorhandler(ce.InternalServerError)
  def internal_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Internal Server Error: {str(error)}")
      return jsonify({"message":  str(error)}), error.status_code

  # Data Validation Error
  @app.errorhandler(ce.DataValidationError)
  def handle_data_validation_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Data Validation Error: {str(error)}")
      return jsonify({"message": str(error)}), error.status_code

  # User Already Exists Error
  @app.errorhandler(ce.UserAlreadyExistsError)
  def handle_user_already_exists_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"User Already Exists Error: {str(error)}")
      return jsonify({"message": str(error)}), error.status_code

  # User not found Error
  @app.errorhandler(ce.UserNotFoundError)
  def handle_user_not_found_error(error):
      from helpers import helper_functions as hf
# 
      return jsonify({"message": str(error)}), error.status_code


  # Token blacklisted Error
  @app.errorhandler(ce.TokenBlacklistError)
  def handle_token_blacklisted_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Token Blacklisted Error: {str(error)}")
      return jsonify({"message": str(error)}), error.status_code

  # Invalid Credentials Error
  @app.errorhandler(ce.InvalidCredentialsError)
  def handle_invalid_credentials_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Invalid Credentials Error: {str(error)}")
      return jsonify({"message": str(error)}), error.status_code


  # Bad Request
  @app.errorhandler(ce.BadRequestError)
  def bad_request_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Bad Request: {str(error)}")
      return jsonify({"message": "Bad Request", "details": str(error)}), 400

  # Resource Not Found
  @app.errorhandler(ce.ResourceNotFoundError)
  def not_found_error(error):
      from helpers import helper_functions as hf
    #   hf.log_event(f"Resource Not Found: {str(error)}")
      return jsonify({"message": "Resource Not Found", "details": str(error)}), 404
