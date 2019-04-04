from flask import render_template, request, redirect, url_for
from application import app, db
from application.deadlines.models import Deadline, Category, Deadline_Category
# TODO:
#from application.categories.forms import CategoryForm

from flask_login import login_required, current_user

@app.route("/categories", methods=["GET"])
@login_required
def categories_index():
    # form that lists all the users categories, with functionality
    # to rename, delete and change their priority
    return render_template("categories/list.html", categories = Category.query.filter(Category.account_id == current_user.id))
