from application import app, db
from flask import render_template, request, redirect, url_for
from application.deadlines.models import Deadline, Deadline_Category
from application.categories.models import Category
from application.deadlines.forms import DeadlineForm, DeadlineCategoryFilterForm, DeadlineNameForm, DeadlineCategoryForm

from sqlalchemy.sql import exists, text

from flask_login import login_required, current_user

@app.route("/")
def deadlines_main():
    return render_template("index.html")

# list all the deadlines from the database
@app.route("/deadlines", methods=["GET"])
@login_required
def deadlines_index():
    category_filter_form = DeadlineCategoryFilterForm(request.form)
    deadline_name_form = DeadlineNameForm(request.form)
    category_form = DeadlineCategoryForm(request.form)
    categories = Category.query.filter(Category.account_id == current_user.id)
    category_options = [(0, '-')]
    for c in categories:
        category_options.append((c.id, c.name))
    category_filter_form.category.choices = category_options
    category_form.category.data = ""

    return render_template("deadlines/list.html", deadlines = Deadline.query.filter(Deadline.account_id == current_user.id),
                            category_filter_form = category_filter_form, 
                            deadline_name_form = DeadlineNameForm(), 
                            category_form = category_form)

# This method is used when filters are applied to the deadline list
@app.route("/deadlines", methods=["POST"])
@login_required
def deadlines_index_filter():
    category_filter_form = DeadlineCategoryFilterForm(request.form)
    category_form = DeadlineCategoryForm(request.form)
    categories = Category.query.filter(Category.account_id == current_user.id)
    category_options = [(0, '-')]
    for c in categories:
        category_options.append((c.id, c.name))
    category_filter_form.category.choices = category_options

    # These fields get some database ids put in them when the filter form is used, 
    # no idea why. This is a bandaid fix for that.
    category_form.category.data = ""

    # prio, cat_prio and date_order are strings, but cat is an integer, 
    prio = category_filter_form.priority.data
    cat = category_filter_form.category.data
    date_order = category_filter_form.date_order.data
    cat_prio = category_filter_form.categorypriority.data

    res = Deadline.query.filter(Deadline.account_id == current_user.id)

    # Applying any possible filters
    if prio != '0':
        res = res.filter(Deadline.priority == prio)

    if cat != 0:
        res = res.filter(Deadline.account_id == current_user.id).filter(Deadline_Category.deadline_id == Deadline.id).filter(Deadline_Category.category_id == cat)

    if cat_prio != '0':
        res = res.filter(Deadline_Category.deadline_id == Deadline.id).filter(Category.id == Deadline_Category.category_id).filter(Category.priority == cat_prio)

    if date_order != '0':
        if date_order == '1':
            res = res.order_by(Deadline.date_time.desc())
        else:
            res = res.order_by(Deadline.date_time.asc())

    return render_template("deadlines/list.html", 
                                    deadlines = res,
                                    category_filter_form = category_filter_form,
                                    deadline_name_form = DeadlineNameForm(),
                                    category_form = category_form)

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

    if not form.validate():
        return render_template("deadlines/new.html", form = form)
    
    d = Deadline(form.name.data, form.date.data, form.hour.data, form.minute.data, form.priority.data)
    d.account_id = current_user.id
    
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

@app.route("/deadlines/<deadline_id>/delete_category", methods=["POST"])
@login_required
def deadline_delete_category(deadline_id):
    form = DeadlineCategoryForm(request.form)

    if not form.validate():
        form.category.data = ""
        return render_template("deadlines/list.html", deadlines = Deadline.query.filter(Deadline.account_id == current_user.id), category_filter_form = DeadlineCategoryFilterForm(), deadline_name_form = DeadlineNameForm(), category_form = form)
    
    if not db.session.query(exists().where(Category.name == form.category.data).where(Category.account_id == current_user.id)).scalar():
        return redirect(url_for("deadlines_index"))

    category = db.session().query(Category).filter(Category.name == form.category.data, Category.account_id == current_user.id).first()

    dc = Deadline_Category.query.filter(Deadline_Category.deadline_id == deadline_id, 
                                        Deadline_Category.category_id == category.id)

    for row in dc:
        db.session.delete(row)

    db.session().commit()

    return redirect(url_for("deadlines_index"))

@app.route("/deadlines/<deadline_id>/add_category", methods=["POST"])
@login_required
def deadline_add_category(deadline_id):
    form = DeadlineCategoryForm(request.form)

    if not form.validate():
        form.category.data = ""
        return render_template("deadlines/list.html", deadlines = Deadline.query.filter(Deadline.account_id == current_user.id), category_filter_form = DeadlineCategoryFilterForm(), deadline_name_form = DeadlineNameForm(), category_form = form)
    
    # if category doesnt exists, it is created. Otherwise the existing category is queried
    if not db.session.query(exists().where(Category.name == form.category.data).where(Category.account_id == current_user.id)).scalar():
        category = Category(form.category.data)
        category.account_id = current_user.id
        db.session.add(category)
        
    category = db.session().query(Category).filter(Category.name == form.category.data, Category.account_id == current_user.id).first()

    d_c = Deadline_Category(deadline_id, category.id)
    db.session().add(d_c)

    db.session.commit()
        
    return redirect(url_for("deadlines_index"))

@app.route("/deadlines/<deadline_id>/done", methods=["POST"])
@login_required
def set_deadline_done(deadline_id):

    d = Deadline.query.get(deadline_id)
    d.done = True
    db.session().commit()

    return redirect(url_for("deadlines_index"))

@app.route("/deadlines/<deadline_id>/undone", methods=["POST"])
@login_required
def set_deadline_undone(deadline_id):

    d = Deadline.query.get(deadline_id)
    d.done = False
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

@app.route("/deadlines/<deadline_id>/rename", methods=["POST"])
@login_required
def rename_deadline(deadline_id):
    form = DeadlineNameForm(request.form)

    if not form.validate():
        form.name.data = ""
        return render_template("deadlines/list.html", deadlines = Deadline.query.filter(Deadline.account_id == current_user.id), category_filter_form = DeadlineCategoryFilterForm(), deadline_name_form = form, category_form = DeadlineCategoryForm())

    d = Deadline.query.get(deadline_id)
    d.name = request.form.get("name")
    db.session().commit()

    return redirect(url_for("deadlines_index"))
