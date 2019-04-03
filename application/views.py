from flask import render_template
from application import app
from application.deadlines.models import Deadline
from application.auth.models import User

@app.route("/")
def index():
    return render_template("index.html", deadline=Deadline, user=User)
