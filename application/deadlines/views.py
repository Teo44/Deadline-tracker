from application import app, db
from flask import render_template, request, redirect, url_for
from application.deadlines.models import Deadline, Category, Deadline_Category
from application.deadlines.forms import DeadlineForm

from sqlalchemy.sql import exists

from flask_login import login_required, current_user

@app.route("/")
def deadlines_main():
    return render_template("index.html")

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
    
    #category = Category.query.filter(Category.name == form.category.data)
    
    if not form.category.data == '':
        if not db.session.query(exists().where(Category.name == form.category.data).where(Category.account_id == current_user.id)).scalar():
            category = Category(form.category.data)
            category.account_id = current_user.id
            db.session.add(category)
        category = Category.query.filter(Category.name == form.category.data, Category.account_id == current_user.id).first()
        d.category_id = category.id
        category.account_id = current_user.id
        

    db.session().add(d)

    if not form.category.data == '':
        deadline = db.session().query(Deadline).filter_by(name = form.name.data).first()
        d_c = Deadline_Category(deadline.id, category.id)
        db.session().add(d_c)

    db.session().commit()

    return redirect(url_for("deadlines_index"))

@app.route("/deadlines/<deadline_id>/done", methods=["POST"])
@login_required
def set_deadline_done(deadline_id):

    d = Deadline.query.get(deadline_id)
    d.done = True
    db.session().commit()

    return redirect(url_for("deadlines_index"))

@app.route("/deadlines/<deadline_id>/delete", methods=["POST"])
@login_required
def delete_deadline(deadline_id):

    dc = Deadline_Category.query.filter(Deadline_Category.deadline_id == deadline_id)

    d = Deadline.query.get(deadline_id)
    for row in dc:
        db.session.delete(row)
    db.session.delete(d)
    db.session().commit()

    return redirect(url_for("deadlines_index"))
