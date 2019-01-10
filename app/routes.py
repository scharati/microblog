from app import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse 
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {"username" : 'Shailesh'}
    posts = [
                {
                    'author': {'username': 'Shailesh'},
                    'body' : '2019 - the panipat of 21st century'
                },
                
                {   
                    'author': {'username' : 'Dhriti'},
                    'body': 'Chinnara kathegalu'
                }
            ]
    return render_template("index.html", title = "Namaste", posts = posts)

@app.route('/login' , methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("index")
        return redirect( next_page )
    return render_template('login.html', title='Sign In', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect( url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        in_username = form.username.data
        in_email = form.email.data
        user = User(username=in_username, email=in_email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect( url_for("index") )
    return render_template ("register.html", title="Register", form=form)

@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts =[
            {"author": user, "body":"My post is here #1"},
            {"author": user, "body": "My post is here #2"}
            ]
    return render_template("user.html", user=user, posts=posts)