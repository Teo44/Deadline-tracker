from application import db
from datetime import datetime
from sqlalchemy.sql import text

class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_to_complete = db.Column(db.Date)
    time_to_complete = db.Column(db.Time)
    name = db.Column(db.String(128), nullable=False)
    priority = db.Column(db.Integer)
    done = db.Column(db.Boolean, nullable=False, default=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


    def __init__(self, name, date_to_complete, priority):
        self.name = name
        self.done = False
        self.date_to_complete = date_to_complete
        self.priority = priority

    @staticmethod
    def get_deadline_category(id):
        stmt = text("SELECT Category.name, Deadline.name FROM Deadline"
                    " JOIN Deadline__Category ON Deadline__Category.deadline_id = Deadline.id"
                    " JOIN Category ON Category.id = Deadline__Category.category_id"
                    " WHERE Deadline__Category.deadline_id = :id").params(id=id)
        res = db.engine.execute(stmt)

        #return res
        for row in res:
            return row[0]

#        # parse the htlm date-string into a list
#        date = date_to_complete.split("-")
#        # sets the day, month and year from the date-list
#        self.date_to_complete = datetime(int(date[0]), int(date[1]), int(date[2]))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    priority = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def getId(self):
        return self.id

    def __init__(self, name):
        self.name = name



    #def __init__(self, name, priority):
    #    self.name = name
    #    self.priority = priority

class Deadline_Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deadline_id = db.Column(db.Integer, db.ForeignKey('deadline.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __init__(self, deadline_id, category_id):
        self.deadline_id = deadline_id
        self.category_id = category_id
