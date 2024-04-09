from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify, request
from validate_email_address import validate_email


def permission_required(*required_permissions):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Implement custom permission check

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def set_current_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        self = args[0]
        self.current_user = get_jwt_identity()
        return fn(*args, **kwargs)

    return wrapper


def require_valid_email(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        email = request.form.get("email")
        if not validate_email(email):
            return jsonify({"error": "Invalid email"}), 400
        return f(*args, **kwargs)

    return decorated_function
