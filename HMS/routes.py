import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from HMS import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from HMS.models import User, Hostel, Payment, Room,Beds
from HMS.static.tourcontent import tourContent
from HMS.static.reportContent import reportContent
from HMS.forms import SignupForm, LoginForm, AnnouncementForm, AddRoomForm, EditRoomForm, UpdateAccountForm, EditRoomPricingForm
from HMS.tables import TotalRoomReport, TotalStudentsReport, TotalFullPaidStudentsReport


@app.route("/")
@app.route("/home")
def home():
  return render_template('Home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user.role == "student":
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('login'))
      else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
    elif user.role == "admin":
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect(url_for('admin'))
      else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))


@app.route("/signup", methods=['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = SignupForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, number=form.number.data, gender=form.gender.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created! You are now able to log in', 'success')
    return redirect(url_for('login'))
  return render_template('signup.html', title='Sign Up', form=form)


@app.route("/about")
def about():
  return render_template('about.html', title="About")


@app.route("/tour")
def tour():
  return render_template('tour.html', title="Take A Tour", tourContent=tourContent)


@app.route("/admin")
@login_required
def admin():
  form2 = AnnouncementForm()
  hostel = Hostel.query.filter_by(hostel_id=current_user.hostel_id).first()
  hostelName = hostel.hostel_name
  totalNumOfRooms = len(hostel.rooms)
  totalNumofStudents = 0
  totalNumOfMales = 0
  totalNumOfFemales = 0
  totalNumofFullyPaid = 0
  for student in hostel.occupants:
    if student.room_id != None:
      totalNumofStudents += 1
    if student.gender == 'M' and student.room_id != None:
      totalNumOfMales += 1
    elif student.gender == 'F' and student.room_id != None:
      totalNumOfFemales += 1

  fullyOccupiedRooms = 0
  occupied_rooms = db.engine.execute("Select * from rooms where rooms.beds = (select count(*) from Users where users.room_id == rooms.room_num)")
  for room in occupied_rooms:
      fullyOccupiedRooms += 1

  for payment in Payment.query.all():
    if payment.amount_remaining == 0:
      totalNumofFullyPaid += 1
  return render_template('admin_home.html', form2=form2, hostelName=hostelName, totalNumOfRooms=totalNumOfRooms,
                         totalNumofStudents=totalNumofStudents, fullyOccupiedRooms=fullyOccupiedRooms, totalNumOfFemales=totalNumOfFemales,
                         totalNumOfMales=totalNumOfMales, totalNumofFullyPaid=totalNumofFullyPaid)


@app.route("/admin/addroom", methods=['GET', 'POST'])
@login_required
def addroom():
  form = AddRoomForm()
  form2 = AnnouncementForm()
  if form.validate_on_submit():
    room_num = form.room_num.data
    beds = form.beds.data
    hostel_id=current_user.hostel_id
    hostel_name=Hostel.query.filter_by(hostel_id=hostel_id).first()
    hostel_name=hostel_name.hostel_name.lower()
    bed=f'{hostel_name}{beds}'
    price = Beds.query.filter_by(beds_id=bed).first()
    price=price.price
    room = Room(room_num=room_num, beds=beds, price=price, hostel_id=current_user.hostel_id)
    db.session.add(room)
    db.session.commit()
    flash('Room successfully added', 'success')
    return redirect(url_for('addroom'))

  return render_template('addroom.html', title='Add Room',
                         form=form, form2=form2, legend='Add New Room')


@app.route("/admin/occupants_details", methods=['GET'])
@login_required
def occupants_details():
  form = AnnouncementForm()
  table = TotalStudentsReport(db.engine.execute("select * from Users where room_id not null"))
  return render_template('occupants_details.html', title='Occupants Details',
                         form2=form, table=table)


@app.route("/admin/viewrooms", methods=['GET'])
@login_required
def viewrooms():
  form2 = AnnouncementForm()
  rooms = Room.query.filter_by(hostel_id=current_user.hostel_id).all()
  return render_template('view_rooms.html', form2=form2, rooms=rooms)


@app.route("/admin/account", methods=['GET', 'POST'])
@login_required
def updateaccount():
  form = UpdateAccountForm()
  form2 = AnnouncementForm()
  if form.validate_on_submit():
    current_user.firstname = form.firstname.data
    current_user.lastname = form.lastname.data
    current_user.number = form.number.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('updateaccount'))
  elif request.method == 'GET':
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    form.number.data = current_user.number
    form.email.data = current_user.email
  return render_template('updateaccount.html', title='Account', form=form, form2=form2)

@app.route('/admin/reports')
@login_required
def reports():
  form2 = AnnouncementForm()
  hostelName = Hostel.query.filter_by(hostel_id=current_user.hostel_id).first().hostel_name
  return render_template('reports.html', title = 'Reports', form2 = form2, hostelName = hostelName, reportContent = reportContent)

@app.route('/admin/reports/detailed_report/<string:id>')
@login_required
def detailed_report(id):
  form2 = AnnouncementForm()
  hostel = Hostel.query.filter_by(hostel_id=current_user.hostel_id).first()
  if(id == "totRooms"):
    table = TotalRoomReport(hostel.rooms)
    return render_template('detailed_reports.html', table = table, form2 = form2)
  if(id == 'totStu'):
    table = TotalStudentsReport(db.engine.execute("select * from Users where room_id not null"))
    return render_template('detailed_reports.html', table=table, form2=form2)
  if(id == 'totStuPaid'):
      table = TotalFullPaidStudentsReport(db.engine.execute("SELECT Users.firstname, Users.lastname,Users.email,Users.number,Payments.amount_paid,Payments.amount_remaining"+
            " FROM Users INNER JOIN Payments ON Payments.user_id = Users.id where Payments.amount_remaining=0"))
      return render_template('detailed_reports.html', table=table, form2=form2)
  if (id == 'totNotFullPaid'):
      table = TotalFullPaidStudentsReport(db.engine.execute(
          "SELECT Users.firstname, Users.lastname,Users.email,Users.number,Payments.amount_paid,Payments.amount_remaining" +
          " FROM Users INNER JOIN Payments ON Payments.user_id = Users.id where Payments.amount_remaining>0"))
      return render_template('detailed_reports.html', table=table, form2=form2)
  if(id == 'totFullRooms'):
    table = TotalRoomReport(db.engine.execute("Select * from rooms where rooms.beds = (select count(*) from Users where users.room_id == rooms.room_num)"))
    return  render_template('detailed_reports.html', table=table, form2=form2)
  if(id == 'totMaleStu'):
    table = TotalStudentsReport(db.engine.execute("select * from Users where gender == 'M' and room_id not null"))
    return render_template('detailed_reports.html', table=table, form2=form2)
  if (id == 'totFemStu'):
    table = TotalStudentsReport(db.engine.execute("select * from Users where gender == 'F' and room_id not null"))
    return render_template('detailed_reports.html', table=table, form2=form2)


@app.route('/admin/viewrooms/room_details/<string:id>')
@login_required
def default_roomview(id):
  form2 = AnnouncementForm()
  room = Room.query.filter_by(room_num=id).first()
  table = TotalStudentsReport(room.occupants)
  return render_template('default_roomview.html', room = room, form2 = form2, table = table)


@app.route('/admin/viewrooms/room_details/<string:id>/update', methods=['GET', 'POST'])
@login_required
def room_details(id):
  global table
  form2 = AnnouncementForm()
  form = EditRoomForm()
  room = Room.query.filter_by(room_num = id).first()
  if form.validate_on_submit():
    room.room_num = form.room_num.data
    room.beds = form.beds.data
    db.session.commit()
    form.room_num.data = room.room_num
    form.beds.data = room.beds
    flash('Room Sucessfully Updated!', 'success')
    return redirect(url_for('room_details', id = room.room_num))
  elif request.method == 'GET':
    form.room_num.data = room.room_num
    form.beds.data = room.beds
    table = TotalStudentsReport(room.occupants)
  return render_template('room_details.html', legend='Edit Room',form=form,form2=form2,table=table, room = room)


@app.route('/admin/viewrooms/room_details/<string:id>/delete', methods=['POST'])
@login_required
def deleteroom(id):
  hostel_id = current_user.hostel_id
  room = Room.query.filter_by(room_num = id, hostel_id = hostel_id).first()
  if len(room.occupants) > 0:
    flash('Room cannot be deleted. Check if room is empty', 'danger')
  else:
    db.session.delete(room)
    db.session.commit()
    flash('Room has been deleted!','success')
    return redirect(url_for('viewrooms'))


@app.route("/admin/editroompricing", methods=['GET', 'POST'])
@login_required
def editroompricing():
  form2 = AnnouncementForm()
  form = EditRoomPricingForm()
  if form.validate_on_submit():
     beds = form.beds.data
     price = form.price.data
     hostel_id = current_user.hostel_id
     db.engine.execute("Update beds set price = "+ str(price) +" where beds.bednum = " + str(beds) +" and beds.hostel_id = " + str(hostel_id))
     db.engine.execute(
       "Update rooms set price = " + str(price) + " where rooms.beds = " + str(beds) + " and rooms.hostel_id = " + str(
         hostel_id))
     flash('Room Pricing have been updated', 'success')
     return redirect(url_for('editroompricing'))

  return render_template('edit_roompricing.html', form2 = form2, form = form, legend = "Edit Room Pricing")


