import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from HMS import app
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('EntryPagesLayout.html')
