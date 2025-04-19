from flask import session, url_for
from functools import wraps
from werkzeug.utils import redirect

def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)

        return redirect(url_for('home'))

    return wrapper

def check_logged_out(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('appointments'))

        return func(*args, **kwargs)

    return wrapper