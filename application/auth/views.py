from flask import render_template, request, redirect, url_for

from application import app
from application.auth.models import User
from application.auth.forms import LoginForm

# handles GET and POST calls to the address /auth/login
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    # TODO: validators for logins

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, error = "Username or password was incorrect")

    print("User: " + user.name)
    return redirect(url_for("index"))
