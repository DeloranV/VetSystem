import mysql.connector

class UseDatabase:
    def __init__(self, config):
        self._config = config

    def __enter__(self):
        self._conn = mysql.connector.connect(**self._config)
        self._cursor = self._conn.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()