from application import db

class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_to_complete = db.Column(db.DateTime)
    name = db.Column(db.String(128), nullable=False)
    priority = db.Column(db.Integer)
    done = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.done = False
