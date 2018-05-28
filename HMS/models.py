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
        return f"Student('{self.firstname}', '{self.lastname}', '{self.email}')"


class room(db.Model):
    room_num = db.Column(db.Integer, primary_key=True)
    beds = db.Column(db.Integer, nullable=False)
    hostel = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Room('{self.room_num}', '{self.beds}', '{self.hostel}')"


class hostel(db.Model):
    hostel_id = db.Column(db.Integer, primary_key=True)
    hostel_name = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return f"Hostel('{self.hostel_id}', '{self.hostel_name}')"


class admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_firstname = db.Column(db.String(30), primary_key=True)
    admin_lastname = db.Column(db.String(30), primary_key=True)
    admin_email = db.Column(db.String(120), unique=True, nullable=False)
    admin_number = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.admin_name}', '{self.admin_number}')"


#class room_occupants(db.Model):
 #   room_num = db.Column(db.Integer)
  #  student_id = db.Column(db.String(30))
    # we would have to check with the counter to make sure the number of people added to the room are less than the number of beds in the room
   # counter = db.Column(db.Integer)

    #def __repr__(self):
     #   return f"Occupant('{self.room_id}')"
