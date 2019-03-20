from application import app, db
from flask import render_template, request, redirect, url_for
from application.deadlines.models import Deadline

# /deadlines list all the deadlines from the database
@app.route("/deadlines", methods=["GET"])
def deadlines_index():
    return render_template("deadlines/list.html", deadlines = Deadline.query.all())

# Function for adding a new deadline, renders new.html
@app.route("/deadlines/new/")
def deadlines_form():
    return render_template("deadlines/new.html")

@app.route("/deadlines/", methods=["POST"])
def deadlines_create():
    d = Deadline(request.form.get("name"), request.form.get("date_to_complete"))

    db.session().add(d)
    db.session().commit()

    return redirect(url_for("deadlines_index"))

@app.route("/deadlines/<deadline_id>/", methods=["POST"])
def set_deadline_done(deadline_id):

    d = Deadline.query.get(deadline_id)
    d.done = True
    db.session().commit()

    return redirect(url_for("deadlines_index"))
