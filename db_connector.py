"""
db_connector.py
----------------
MySQL සහ PostgreSQL දෙකටම connection handle කරන module එක.
config.yaml එකේ "database.type" value එක අනුව නිවැරදි driver එක තෝරගන්නවා.
"""

import sys


class DatabaseConnector:
    """
    Database connection එක open/close කරන, query run කරන wrapper class එක.
    MySQL සහ PostgreSQL දෙකෙන්ම syntax වෙනස්කම් (e.g. placeholder style)
    මේ class එක internal ව handle කරනවා.
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
        """Database එකට connect වෙනවා. Fail උනොත් clear error message එකක් දෙනවා."""
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
                    "config.yaml එකේ 'mysql' හෝ 'postgresql' ලෙස set කරන්න."
                )

            print(f"[OK] {self.db_type.upper()} database එකට සාර්ථකව connect විය: {self.database}")

        except Exception as e:
            print(f"[ERROR] Database connection එක fail විය: {e}", file=sys.stderr)
            sys.exit(1)

    def execute_query(self, query: str, params: tuple = None):
        """SELECT query එකක් run කරලා results ලබාදෙනවා (list of dicts)."""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Query execution fail විය: {e}", file=sys.stderr)
            sys.exit(1)

    def execute_write(self, query: str, params: tuple = None):
        """DELETE/UPDATE වගේ write query එකක් run කරලා commit කරනවා."""
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            print(f"[ERROR] Write operation fail විය, rollback කරන ලදී: {e}", file=sys.stderr)
            sys.exit(1)

    def get_placeholder(self) -> str:
        """MySQL vs PostgreSQL query placeholder syntax වෙනස (%s දෙකෙන්ම common)."""
        return "%s"

    def close(self):
        """Connection එක close කරනවා."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("[OK] Database connection එක close කරන ලදී.")
