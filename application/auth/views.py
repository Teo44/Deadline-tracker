from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegistrationForm

@app.route("/auth/registration", methods = ["GET", "POST"])
def auth_registration():
    if request.method == "GET":
        return render_template("auth/registrationform.html", form=RegistrationForm())

    form = RegistrationForm(request.form)
    print(form.validate())
    if not form.validate():
        return render_template("auth/registrationform.html", form = form)
    
    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template("auth/registrationform.html", form = form, 
                                error = "Username is already taken")
    
    u = User(form.username.data, form.password.data)

    db.session().add(u)
    db.session().commit()

    # logging the user in after account creation
    login_user(u)
    return redirect(url_for("index"))
    
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    if not form.validate():
        return render_template("auth/loginform.html", form = form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, 
            error = "Username or password was incorrect")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
