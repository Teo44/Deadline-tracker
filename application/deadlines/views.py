from application import app, db
from flask import render_template, request, redirect, url_for
from application.deadlines.models import Deadline, Category, Deadline_Category
from application.deadlines.forms import DeadlineForm, DeadlineCategoryFilterForm

from sqlalchemy.sql import exists, text

from flask_login import login_required, current_user

@app.route("/")
def deadlines_main():
    return render_template("index.html")

# /deadlines list all the deadlines from the database
@app.route("/deadlines", methods=["GET"])
@login_required
def deadlines_index():
    category_filter_form = DeadlineCategoryFilterForm(request.form)
    categories = Category.query.filter(Category.account_id == current_user.id)
    category_options = [(0, '-')]
    for c in categories:
        category_options.append((c.id, c.name))
    category_filter_form.category.choices = category_options
    #category_filter_form.category.choices = [(c.id, c.name) for c in categories]
    # show all the deadlines for all users
    #return render_template("deadlines/list.html", deadlines = Deadline.query.all())
    # only show deadlines matching current user
    return render_template("deadlines/list.html", deadlines = Deadline.query.filter(Deadline.account_id == current_user.id),
                            category_filter_form = category_filter_form)

@app.route("/deadlines", methods=["POST"])
@login_required
def deadlines_index_filter():
    category_filter_form = DeadlineCategoryFilterForm(request.form)
    categories = Category.query.filter(Category.account_id == current_user.id)
    category_options = [(0, '-')]
    for c in categories:
        category_options.append((c.id, c.name))
    category_filter_form.category.choices = category_options

    # NOTE: prio and date_order are strings, cat is an integer...
    prio = category_filter_form.priority.data
    cat = category_filter_form.category.data
    date_order = category_filter_form.date_order.data

    if cat != 0 and prio != '0' and date_order != '0':
        if date_order == '1':
            res = Deadline.query.filter(Deadline.account_id == current_user.id).filter(Deadline_Category.deadline_id == Deadline.id).filter(Deadline_Category.category_id == cat).filter(Deadline.priority == prio).order_by(Deadline.date_time.desc())
        else:
            res = Deadline.query.filter(Deadline.account_id == current_user.id).filter(Deadline_Category.deadline_id == Deadline.id).filter(Deadline_Category.category_id == cat).filter(Deadline.priority == prio).order_by(Deadline.date_time.asc())
    elif cat != 0 and prio != '0':
        res = Deadline.query.filter(Deadline.account_id == current_user.id).filter(Deadline_Category.deadline_id == Deadline.id).filter(Deadline_Category.category_id == cat).filter(Deadline.priority == prio)
    elif cat != 0 and date_order != 0:
        if date_order == '1':
            res = Deadline.query.filter(Deadline.account_id == current_user.id).filter(Deadline_Category.deadline_id == Deadline.id).filter(Deadline_Category.category_id == cat).order_by(Deadline.date_time.desc())
        else:
            res = Deadline.query.filter(Deadline.account_id == current_user.id).filter(Deadline_Category.deadline_id == Deadline.id).filter(Deadline_Category.category_id == cat).order_by(Deadline.date_time.asc())
    elif prio != '0' and date_order != '0':
        if date_order == '1':
            res = Deadline.query.filter(Deadline.account_id == current_user.id, Deadline.priority == prio).order_by(Deadline.date_time.desc())
        else:
            res = Deadline.query.filter(Deadline.account_id == current_user.id, Deadline.priority == prio).order_by(Deadline.date_time.asc())
    elif cat != 0:
        res = Deadline.query.filter(Deadline.account_id == current_user.id).filter(Deadline_Category.deadline_id == Deadline.id).filter(Deadline_Category.category_id == cat)
    elif prio != '0':
        res = Deadline.query.filter(Deadline.account_id == current_user.id, Deadline.priority == prio)
    elif date_order != '0':
        if date_order == '1':
            res = Deadline.query.filter(Deadline.account_id == current_user.id).order_by(Deadline.date_time.desc())
        else:
            res = Deadline.query.filter(Deadline.account_id == current_user.id).order_by(Deadline.date_time.asc())
    else:
        res = Deadline.query.filter(Deadline.account_id == current_user.id)

    return render_template("deadlines/list.html", 
                                    deadlines = res,
                                    category_filter_form = category_filter_form)

# Function for adding a new deadline, renders new.html
@app.route("/deadlines/new/")
@login_required
def deadlines_form():
    return render_template("deadlines/new.html", form = DeadlineForm())

# this method is for when the deadlines are filtered
@app.route("/deadlines/create", methods=["POST"])
@login_required
def deadlines_create():
    form = DeadlineForm(request.form)

    print("before validation")
    
    #if not form.validate():
    #    return render_template("deadlines/new.html", form = form)

    print("validated")
    
    d = Deadline(form.name.data, form.date.data, form.hour.data, form.minute.data, form.priority.data)
    
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
