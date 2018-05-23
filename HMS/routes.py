import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from HMS import app
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/login")
def home():
    return render_template('layout.html')
