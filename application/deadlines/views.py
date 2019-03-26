from application import app, db
from flask import render_template, request, redirect, url_for
from application.deadlines.models import Deadline
from application.deadlines.forms import DeadlineForm

from flask_login import login_required, current_user

# /deadlines list all the deadlines from the database
@app.route("/deadlines", methods=["GET"])
@login_required
def deadlines_index():
    # show all the deadlines for all users
    #return render_template("deadlines/list.html", deadlines = Deadline.query.all())
    # only show deadlines matching current user
    return render_template("deadlines/list.html", deadlines = Deadline.query.filter(Deadline.account_id == current_user.id))

# Function for adding a new deadline, renders new.html
@app.route("/deadlines/new/")
@login_required
def deadlines_form():
    return render_template("deadlines/new.html", form = DeadlineForm())

@app.route("/deadlines/", methods=["POST"])
@login_required
def deadlines_create():
    form = DeadlineForm(request.form)
    
    if not form.validate():
        return render_template("deadlines/new.html", form = form)
    
    d = Deadline(form.name.data, form.date.data, form.priority.data)
#    d = Deadline(request.form.get("name"), request.form.get("date_to_complete"))
    
    d.account_id = current_user.id

    db.session().add(d)
    db.session().commit()

    return redirect(url_for("deadlines_index"))

@app.route("/deadlines/<deadline_id>/", methods=["POST"])
@login_required
def set_deadline_done(deadline_id):

    d = Deadline.query.get(deadline_id)
    d.done = True
    db.session().commit()

    return redirect(url_for("deadlines_index"))
