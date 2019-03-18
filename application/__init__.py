from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///deadlines.db"
# Set SQLA to print out all SQL-queries
app.config["SQLAlCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.deadlines import models
from application.deadlines import views

# Creating tables
db.create_all()
