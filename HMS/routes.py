import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from HMS import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from HMS.models import User
from HMS.static.tourcontent import tourContent
from HMS.forms import SignupForm, LoginForm, AnnouncementForm, AddRoomForm, EditRoomForm, UpdateAccountForm

rooms = [
    {"name": "GF1", "beds": 2}, {"name": "GF2", "beds": 4}, {"name": "GF3", "beds": 3},
    {"name": "FF1", "beds": 1}, {"name": "FF2", "beds": 4}, {"name": "FF3", "beds": 2},
    {"name": "SF1", "beds": 3},
]


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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('login'))
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
    return render_template('admin_home.html', form2=form2)


@app.route("/admin/addroom")
@login_required
def addroom():
    form = AddRoomForm()
    form2 = AnnouncementForm()
    return render_template('addroom.html', title='Add Room',
                           form=form, form2=form2, legend='Add New Room')


@app.route("/admin/editroom")
@login_required
def editroom():
    form = EditRoomForm()
    form2 = AnnouncementForm()
    persons = [dict(name='Name1', paid=2600, remain=1000, action='none'),
               dict(name='Name2', paid=2600, remain=1000, action='none'),
               dict(name='Name3', paid=2600, remain=1000, action='none'),
               dict(name='Name4', paid=2600, remain=1000, action='none')]

    return render_template('editroom.html', title='Add Room',
                           form=form, form2=form2, legend='Edit Room', persons=persons)


@app.route("/admin/occupants_details")
@login_required
def occupants_details():
    form = AnnouncementForm()
    persons = [dict(name='Name1', paid=2600, remain=1000, action='none'),
               dict(name='Name2', paid=2600, remain=1000, action='none'),
               dict(name='Name3', paid=2600, remain=1000, action='none'),
               dict(name='Name4', paid=2600, remain=1000, action='none'),
               dict(name='Name5', paid=2600, remain=1000, action='none'),
               dict(name='Name6', paid=2600, remain=1000, action='none'),
               dict(name='Name7', paid=2600, remain=1000, action='none'),
               dict(name='Name8', paid=2600, remain=1000, action='none'),
               dict(name='Name9', paid=2600, remain=1000, action='none'),
               dict(name='Name10', paid=2600, remain=1000, action='none'),
               dict(name='Name10', paid=2600, remain=1000, action='none'),
               dict(name='Name10', paid=2600, remain=1000, action='none'),
               dict(name='Name10', paid=2600, remain=1000, action='none'),
               dict(name='Name10', paid=2600, remain=1000, action='none')]
    return render_template('occupants_details.html', title='Add Room',
                           form2=form, persons=persons)


@app.route("/admin/viewrooms")
@login_required
def viewrooms():
    form2 = AnnouncementForm()
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
