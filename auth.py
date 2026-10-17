from functools  import wraps
from flask import session,redirect,url_for, render_template

def login_required(function):
    @wraps(function)
    def wrapper(*args,**kwargs):

        if "username" not in session:
            return redirect(url_for("auth.login"))

        return function(*args,**kwargs)
    return wrapper

def admin_required(function):
    @wraps(function)
    def wrapper(*args,**kwargs):

        if "username" not in session:
            return redirect(url_for("auth.login"))

        if session.get("role") != "admin":
            return render_template("403.html"),403

        return function(*args,**kwargs)
    return wrapper

