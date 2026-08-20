"""
User repository for database operations
Handles all user CRUD operations
"""
from database.database import Database


class UserRepository:
    """
    Repository for user database operations
    Implements CRUD operations for user management
    """

    def __init__(self):
        """Initialize repository with database connection"""
        self.db = Database()

    def get_all(self):
        """
        Get all users
        
        Returns:
            list: All users ordered by username
        """
        rows = self.db.fetchall("""
            SELECT *
            FROM users
            ORDER BY username
        """)
        return rows

    def get_by_username(self, username):
        """
        Get user by username
        
        Args:
            username (str): Username to search for
            
        Returns:
            sqlite3.Row: User row or None
        """
        return self.db.fetchone("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (username,))

    def get_by_id(self, user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID to search for
            
        Returns:
            sqlite3.Row: User row or None
        """
        return self.db.fetchone("""
            SELECT *
            FROM users
            WHERE id = ?
        """, (user_id,))

    def add(self, username, password, role, status="Active"):
        """
        Add new user
        
        Args:
            username (str): Username
            password (str): Password (should be hashed)
            role (str): User role
            status (str): User status (default: Active)
        """
        self.db.execute("""
            INSERT INTO users
            (username, password, role, status)
            VALUES (?, ?, ?, ?)
        """, (username, password, role, status))

    def update(self, user_id, username, role, status):
        """
        Update user information
        
        Args:
            user_id (int): User ID
            username (str): New username
            role (str): New role
            status (str): New status
        """
        self.db.execute("""
            UPDATE users
            SET
                username = ?,
                role = ?,
                status = ?
            WHERE id = ?
        """, (username, role, status, user_id))

    def change_password(self, user_id, password):
        """
        Change user password
        
        Args:
            user_id (int): User ID
            password (str): New password (should be hashed)
        """
        self.db.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (password, user_id))

    def delete(self, user_id):
        """
        Delete user by ID
        
        Args:
            user_id (int): User ID to delete
        """
        self.db.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (user_id,))
