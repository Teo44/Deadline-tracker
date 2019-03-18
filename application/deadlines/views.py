from application import app, db
from flask import render_template, request
from application.deadlines.models import Deadline

# Function for adding a new deadline, renders new.html
@app.route("/deadlines/new/")
def deadlines_form():
    return render_template("deadlines/new.html")

@app.route("/deadlines/", methods=["POST"])
def deadlines_create():
    d = Deadline(request.form.get("name"))

    db.session().add(d)
    db.session().commit()

    return "hello world 321"
