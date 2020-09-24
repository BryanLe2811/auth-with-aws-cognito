from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    useremail = db.Column(db.String(120))
    role = db.Column(db.String(32), default='customer')

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(id)