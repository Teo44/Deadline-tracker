# flask application
from flask import Flask
app = Flask(__name__)

# database
from flask_sqlalchemy import SQLAlchemy
import os
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    # Set SQLA to print out all SQL-queries
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///deadlines.db"
    app.config["SQLAlCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# Database tracker's components
from application import views

from application.deadlines import models
from application.deadlines import views

# database model for users
from application.auth import models
from application.auth import views

# database model for deadline categories
from application.categories import views

# registeration
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login first"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Creating tables
try:
    db.create_all()
except:
    pass
