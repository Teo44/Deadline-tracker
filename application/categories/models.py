from application import db
from sqlalchemy.sql import text

import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    priority = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def getId(self):
        return self.id

    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def get_deadline_count(category_id):
        stmt = text("SELECT COUNT(*) FROM Deadline JOIN Deadline__category ON Deadline__category.deadline_id = Deadline.id WHERE Deadline__category.category_id = :id").params(id=category_id)
        res = db.engine.execute(stmt)

        for row in res:
            return row[0]

    @staticmethod
    def get_next_deadline(category_id):
        date = datetime.datetime.now().date()
        stmt = text("SELECT Deadline.name FROM Category"
                    " JOIN Deadline__category ON Deadline__category.category_id = Category.id"
                    " JOIN Deadline ON Deadline.id = Deadline__category.deadline_id"
                    " WHERE Category.id = :id AND Deadline.date_time >= :date"
                    " ORDER BY Deadline.date_time ASC").params(date=date, id=category_id)
        res = db.engine.execute(stmt)

        for row in res: 
            return row[0]

