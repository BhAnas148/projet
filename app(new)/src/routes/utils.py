from flask import session, redirect, url_for
from functools import wraps

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'LOGGED_IN' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('users.login'))

    return wrap