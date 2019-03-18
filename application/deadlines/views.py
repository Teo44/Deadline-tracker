from application import app, db
from flask import render_template, request, redirect, url_for
from application.deadlines.models import Deadline

@app.route("/deadlines", methods=["GET"])
def deadlines_index():
    return render_template("deadlines/list.html", deadlines = Deadline.query.all())

# Function for adding a new deadline, renders new.html
@app.route("/deadlines/new/")
def deadlines_form():
    return render_template("deadlines/new.html")

@app.route("/deadlines/", methods=["POST"])
def deadlines_create():
    d = Deadline(request.form.get("name"))

    db.session().add(d)
    db.session().commit()

    return redirect(url_for("deadlines_index"))
