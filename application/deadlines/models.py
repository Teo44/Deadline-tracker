from application import db
from datetime import datetime, time
from sqlalchemy.sql import text

import datetime

class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    name = db.Column(db.String(128), nullable=False)
    priority = db.Column(db.Integer)
    done = db.Column(db.Boolean, nullable=False, default=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, name, date, hour, minute, priority):
        self.name = name
        self.done = False
        self.priority = priority
        self.date_time = datetime.datetime(date.year, date.month, date.day, int(hour), int(minute))

    @staticmethod
    def get_deadline_category(id):
        stmt = text("SELECT Category.name, Deadline.name FROM Deadline"
                    " JOIN Deadline__Category ON Deadline__Category.deadline_id = Deadline.id"
                    " JOIN Category ON Category.id = Deadline__Category.category_id"
                    " WHERE Deadline__Category.deadline_id = :id").params(id=id)
        res = db.engine.execute(stmt)

        return res

    @staticmethod
    def get_deadline_count():
        stmt = text("SELECT COUNT(*) FROM Deadline")
        res = db.engine.execute(stmt)

        for row in res:
            return row[0]
    
    @staticmethod
    def get_done_deadline_count():
        stmt = text("SELECT COUNT(*) FROM Deadline"
                    " WHERE Deadline.done")
        res = db.engine.execute(stmt)

        for row in res:
            return row[0]

    @staticmethod
    def get_user_count_with_undone_tasks():
        stmt = text("SELECT COUNT(DISTINCT Account.id) FROM Account" 
                    " JOIN Deadline ON Deadline.account_id = Account.id"
                    " WHERE NOT Deadline.done")
        res = db.engine.execute(stmt)

        for row in res:
            return row[0]

class Deadline_Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deadline_id = db.Column(db.Integer, db.ForeignKey('deadline.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __init__(self, deadline_id, category_id):
        self.deadline_id = deadline_id
        self.category_id = category_id
