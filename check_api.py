from flask import request
from functools import wraps
from mysql.connector import DatabaseError
from dbContextManager import UseDatabase

def check_api_key(app):
    def decorator_creator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            kv_arguments = request.args.get('key','')
            try:
                with UseDatabase(app.config['dbconfig']) as cursor:
                    _SQL = '''SELECT * FROM users WHERE api_key=%s'''

                    cursor.execute(_SQL, (kv_arguments,))
                    results = cursor.fetchall()

                    if len(results) != 0 and kv_arguments:
                        return func(*args, **kwargs)
                    else:
                        return "Invalid API Key"
            except DatabaseError:
                return "Unable to connect to the database", 404
        return wrapper
    return decorator_creator