from flask import (
    Blueprint, 
    render_template,
    request,
    redirect,   
    url_for,
    flash,
    session
    )

from werkzeug.security import check_password_hash

from database import (
    create_user,
    get_user_by_email,
    get_user_by_username
)

from forms import LoginForm, RegisterForm

auth_bp = Blueprint(
    "auth",
    __name__
)

# LOGIN
@auth_bp.route("/login",methods=["GET","POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = get_user_by_username(username)

        if user is None:
            flash("Invalid Username or Password","danger")

            return redirect(url_for("auth.login"))

        password_is_correct = check_password_hash(user["password"],password)

        if not password_is_correct:
            flash("Invalid Username or Password","danger")

            return redirect(url_for("auth.login"))

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        flash("Login Successful","success")


        if user["role"] == "admin":
            return redirect(url_for("home"))

        return redirect(url_for("student.student_list"))

    return render_template("login.html",form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    # NEW: Create an instance of RegisterForm from forms.py
    form = RegisterForm()

    # OLD: if request.method == "POST":
    # NEW: Validate submitted data using RegisterForm
    if form.validate_on_submit():

        # OLD: username = request.form.get("username")
        # OLD: email = request.form.get("email")
        # OLD: password = request.form.get("password")
        # OLD: confirm_password = request.form.get("confirm_password")

        # NEW: Get validated data from RegisterForm
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # OLD: Manual password comparison
        # if password != confirm_password:
        #     flash("Password do not match", "warning")
        #     return redirect(url_for("auth.register"))

        # NEW: EqualTo validator in RegisterForm checks passwords match

        existing_username = get_user_by_username(username)

        if existing_username:
            flash("Username is already exists", "warning")
            return redirect(url_for("auth.register"))

        existing_email = get_user_by_email(email)

        if existing_email:
            flash("Email is already exists", "warning")
            return redirect(url_for("auth.register"))

        # Existing database function remains unchanged
        create_user(username, email, password)

        flash("Registration Successful. Please Login", "success")

        return redirect(url_for("auth.login"))

    # NEW: Pass the form to register.html
    return render_template("register.html", form=form)

@auth_bp.route("/logout")
def logout():
    session.clear()

    flash("You have been Logged Out","info")

    return redirect(url_for("auth.login"))