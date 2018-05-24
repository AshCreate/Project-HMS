import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from HMS import app
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('Home.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/tour")
def tour():
    return render_template('tour.html', title="Take A Tour")
