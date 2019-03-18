from application import app
from flask import render_template, request

@app.route("/deadlines/new/")
def deadline_form():
    return render_template("deadlines/new.html")

@app.route("/deadlines/", methods=["POST"])
def tasks_create():
    print(request.form.get("name"))

    return "hello world 321"
