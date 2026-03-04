from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if "user_id" not in session:
                return redirect(url_for("auth.login"))

            if session.get("role") not in roles:
                return redirect(url_for("auth.login"))

            return f(*args, **kwargs)
        return decorated_function
    return wrapper