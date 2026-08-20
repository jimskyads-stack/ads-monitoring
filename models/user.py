"""
User model for Flask-Login authentication
"""
from flask_login import UserMixin


class User(UserMixin):
    """
    User class implementing Flask-Login UserMixin
    Provides authentication properties and methods
    """

    def __init__(self, username, role):
        """
        Initialize User
        
        Args:
            username (str): Username identifier
            role (str): User role (Admin, Supervisor, Viewer, etc.)
        """
        self.id = username
        self.username = username
        self.role = role

    @property
    def is_authenticated(self):
        """User is authenticated"""
        return True

    @property
    def is_active(self):
        """User account is active"""
        return True

    @property
    def is_anonymous(self):
        """User is not anonymous"""
        return False

    def get_id(self):
        """Get unique user identifier"""
        return self.username
