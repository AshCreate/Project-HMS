import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from HMS import app
from flask_login import login_user, current_user, logout_user, login_required


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
    return render_template('tour.html', title="Take A Tour", tourContent = tourContent)
