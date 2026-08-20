"""
SQLite Database connection and query manager
"""
import sqlite3
from config import DATABASE_NAME


class Database:
    """
    Database connection manager for SQLite
    Handles connection pooling and query execution
    """

    def _connect(self):
        """
        Create a new database connection
        
        Returns:
            sqlite3.Connection: Database connection with row factory
        """
        conn = sqlite3.connect(str(DATABASE_NAME))
        conn.row_factory = sqlite3.Row
        return conn

    def execute(self, query, values=()):
        """
        Execute a query (INSERT, UPDATE, DELETE)
        
        Args:
            query (str): SQL query string
            values (tuple): Query parameters
        """
        with self._connect() as conn:
            conn.execute(query, values)
            conn.commit()

    def fetchall(self, query, values=()):
        """
        Fetch all results from a query
        
        Args:
            query (str): SQL query string
            values (tuple): Query parameters
            
        Returns:
            list: List of sqlite3.Row objects
        """
        with self._connect() as conn:
            return conn.execute(query, values).fetchall()

    def fetchone(self, query, values=()):
        """
        Fetch single result from a query
        
        Args:
            query (str): SQL query string
            values (tuple): Query parameters
            
        Returns:
            sqlite3.Row: Single row or None
        """
        with self._connect() as conn:
            return conn.execute(query, values).fetchone()
