from application import db
from sqlalchemy.sql import text

class User(db.Model):

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    deadlines = db.relationship("Deadline", backref='account', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def get_account_count():
        stmt = text("SELECT COUNT(*) FROM Account")
        res = db.engine.execute(stmt)

        for row in res:
            return row[0]
