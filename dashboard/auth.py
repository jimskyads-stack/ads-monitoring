"""
Authentication and authorization decorators
"""
from functools import wraps
from flask_login import current_user
from flask import abort


def role_required(*roles):
    """
    Decorator to check if user has required role(s)
    
    Usage:
        @role_required("Admin", "Supervisor")
        def protected_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check if user is authenticated
            if not current_user.is_authenticated:
                abort(401)  # Unauthorized

            # Check if user has required role
            if current_user.role not in roles:
                abort(403)  # Forbidden

            return f(*args, **kwargs)

        return wrapper

    return decorator
