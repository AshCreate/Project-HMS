from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from HMS import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return studentUser.query.get(int(user_id))


class studentUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"


class room(db.Model, UserMixin):
    room_num = db.Column(db.Integer, primary_key=True)
    beds = db.Column(db.Integer, nullable=False)
    hostel = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"


class hostel(db.Model, UserMixin):
    hostel_id = db.Column(db.Integer, primary_key=True)
    hostel_name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"


class admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(30), primary_key=True)
    admin_email = db.Column(db.String(120), unique=True, nullable=False)
    admin_number = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"
