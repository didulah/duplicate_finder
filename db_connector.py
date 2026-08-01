"""
db_connector.py
----------------
Handles connections for both MySQL and PostgreSQL.
Picks the correct driver based on the "database.type" value in config.yaml.
"""

import sys


class DatabaseConnector:
    """
    Wrapper class that opens/closes the database connection and runs queries.
    Internally handles the syntax differences between MySQL and PostgreSQL
    (e.g. placeholder style).
    """

    def __init__(self, db_config: dict):
        self.db_type = db_config.get("type", "mysql").lower()
        self.host = db_config["host"]
        self.port = db_config["port"]
        self.user = db_config["user"]
        self.password = db_config["password"]
        self.database = db_config["database"]
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connects to the database. Prints a clear error message on failure."""
        try:
            if self.db_type == "mysql":
                import mysql.connector
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
                self.cursor = self.connection.cursor(dictionary=True)

            elif self.db_type == "postgresql":
                import psycopg2
                import psycopg2.extras
                self.connection = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    dbname=self.database,
                )
                self.cursor = self.connection.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )

            else:
                raise ValueError(
                    f"Unsupported database type: '{self.db_type}'. "
                    "Set this to 'mysql' or 'postgresql' in config.yaml."
                )

            print(f"[OK] Connected successfully to {self.db_type.upper()} database: {self.database}")

        except Exception as e:
            print(f"[ERROR] Database connection failed: {e}", file=sys.stderr)
            sys.exit(1)

    def execute_query(self, query: str, params: tuple = None):
        """Runs a SELECT query and returns the results (list of dicts)."""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Query execution failed: {e}", file=sys.stderr)
            sys.exit(1)

    def execute_write(self, query: str, params: tuple = None):
        """Runs a write query (DELETE/UPDATE) and commits it."""
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            print(f"[ERROR] Write operation failed, rolled back: {e}", file=sys.stderr)
            sys.exit(1)

    def get_placeholder(self) -> str:
        """MySQL vs PostgreSQL query placeholder syntax (%s is common to both)."""
        return "%s"

    def close(self):
        """Closes the connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("[OK] Database connection closed.")
