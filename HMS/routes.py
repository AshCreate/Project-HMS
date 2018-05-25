import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from HMS import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from HMS.models import studentUser
from HMS.forms import SignupForm, LoginForm
from flask_mail import Message


tourContent = [
    {
        "pic": "static/img/back9.jpg",
        "title": "Hosanna",
        "body" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum in lectus auctor,"+
                 " consequat tellus vitae, feugiat urna. Etiam velit risus, porta eget nisi non, egestas posuere justo."+
                 " Nam ornare felis sit amet vehicula accumsan. Quisque at rhoncus est, ullamcorper condimentum tellus. "+
                 "Proin facilisis, nisi non bibendum interdum, urna purus efficitur neque, volutpat ornare dui nunc et diam."+
                 " Proin bibendum mauris ac mollis viverra. Nam tincidunt, purus sed bibendum suscipit, est ante eleifend elit,"+
                 " at accumsan augue diam et ligula. Proin accumsan sem non finibus interdum. Etiam placerat metus in dui mollis,"+
                 " id rutrum ligula imperdiet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis"+
                 " egestas. Sed tincidunt varius eros ac dapibus. Sed volutpat a justo at lobortis. Integer eu nisl felis."
    },

    {
        "pic": "static/img/back11.jpg",
        "title": "Dufie",
        "body" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum in lectus auctor,"+
                 " consequat tellus vitae, feugiat urna. Etiam velit risus, porta eget nisi non, egestas posuere justo."+
                 " Nam ornare felis sit amet vehicula accumsan. Quisque at rhoncus est, ullamcorper condimentum tellus. "+
                 "Proin facilisis, nisi non bibendum interdum, urna purus efficitur neque, volutpat ornare dui nunc et diam."+
                 " Proin bibendum mauris ac mollis viverra. Nam tincidunt, purus sed bibendum suscipit, est ante eleifend elit,"+
                 " at accumsan augue diam et ligula. Proin accumsan sem non finibus interdum. Etiam placerat metus in dui mollis,"+
                 " id rutrum ligula imperdiet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis"+
                 " egestas. Sed tincidunt varius eros ac dapibus. Sed volutpat a justo at lobortis. Integer eu nisl felis."
    },

    {
        "pic": "static/img/back6.jpg",
        "title": "Charlotte",
        "body" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum in lectus auctor,"+
                 " consequat tellus vitae, feugiat urna. Etiam velit risus, porta eget nisi non, egestas posuere justo."+
                 " Nam ornare felis sit amet vehicula accumsan. Quisque at rhoncus est, ullamcorper condimentum tellus. "+
                 "Proin facilisis, nisi non bibendum interdum, urna purus efficitur neque, volutpat ornare dui nunc et diam."+
                 " Proin bibendum mauris ac mollis viverra. Nam tincidunt, purus sed bibendum suscipit, est ante eleifend elit,"+
                 " at accumsan augue diam et ligula. Proin accumsan sem non finibus interdum. Etiam placerat metus in dui mollis,"+
                 " id rutrum ligula imperdiet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis"+
                 " egestas. Sed tincidunt varius eros ac dapibus. Sed volutpat a justo at lobortis. Integer eu nisl felis."
    }
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
        user = studentUser.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = studentUser(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/tour")
def tour():
    return render_template('tour.html', title="Take A Tour", tourContent = tourContent)
