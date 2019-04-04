from flask import render_template, request, redirect, url_for
from application import app, db
from application.deadlines.models import Deadline, Category, Deadline_Category
# TODO:CategoryNameForm
from application.categories.forms import CategoryPriorityForm

from flask_login import login_required, current_user

@app.route("/categories", methods=["GET"])
@login_required
def categories_index():
    # form that lists all the users categories, with functionality
    # to rename, delete and change their priority
    return render_template("categories/list.html", categories = Category.query.filter(Category.account_id == current_user.id), prioForm = CategoryPriorityForm())

@app.route("/categories/<category_id>/delete", methods=["POST"])
@login_required
def delete_category(category_id):

    c = Category.query.get(category_id)
    db.session.delete(c)
    db.session().commit()

    return redirect(url_for("categories_index"))

@app.route("/categories/<category_id>/priority", methods=["POST"])
@login_required
def categories_set_priority(category_id):
    form = CategoryPriorityForm(request.form)

    c = Category.query.get(category_id)
    c.priority = request.form.get("priority")

    db.session().commit()

    return redirect(url_for("categories_index"))
