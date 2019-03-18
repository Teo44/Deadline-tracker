from application import app
from flask import render_template, request

@app.route("/deadlines/new/")
def deadlines_form():
    return render_template("deadlines/new.html")

@app.route("/deadlines/", methods=["POST"])
def deadlines_create():
    print(request.form.get("name"))

    return "hello world 321"
