from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from HMS import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(10), nullable=False, default= "student")
    password = db.Column(db.String(60), nullable=False)
    hostel_id = db.Column(db.Integer, db.ForeignKey('hostel.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    payment = db.relationship('payment', backref='user')
    images = db.relationship('Images', backref='user')
    announcements = db.relationship('Announcement', backref = 'user')

    def __repr__(self):
        return f"Student('{self.firstname}', '{self.lastname}', '{self.email}')"


class room(db.Model):
    room_num = db.Column(db.String, primary_key=True)
    beds = db.Column(db.Integer, nullable=False)
    hostel_id = db.Column(db.Integer, db.ForeignKey('hostel'))
    occupants = db.relationship('User', backref='room')
    price = db.Column(db.Integer, nullable= False)

    def __repr__(self):
        return f"Room('{self.room_num}', '{self.beds}', '{self.hostel}')"


class hostel(db.Model):
    hostel_id = db.Column(db.Integer, primary_key=True)
    hostel_name = db.Column(db.String(30), unique=True)
    occupants = db.relationship('User', backref = 'hostel')
    rooms = db.relationship('hostel', backref = 'hostel')

    def __repr__(self):
        return f"Hostel('{self.hostel_id}', '{self.hostel_name}')"

class payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True),
    amount_paid = db.Column( db.Integer, nullable=False),
    amount_remaining = db.Column(db.Integer, nullable=False),

    def __repr__(self):
        return f"Payments('{self.payment_id}', '{self.user_id}', '{self.amount_paid}')"

class Images(db.Model):
    image_id = db.Column(db.Integer, primary_key= True)
    image_file = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    processed = db.Column(db.String(10), nullable= False, default="False")

    def __repr__(self):
        return f"Images('{self.image_id}', '{self.date_posted}', '{self.processed}')"

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Announcements('{self.subject}', '{self.date_posted}')"

