from app import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse 
from app.forms import LoginForm, RegisterForm,  EditProfileForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from models import User,Post
from datetime import datetime
import pdb


@app.route('/')
@app.route('/index', methods = ["GET", "POST"])
@login_required
def index():
    form = PostForm()
    posts = current_user.followed_posts()
    if form.validate_on_submit():
       post = Post(body=form.post.data, author=current_user)
       db.session.add(post)
       db.session.commit()
       flash("Your post in new live!")
       posts = current_user.followed_posts()
       return redirect(url_for("index"))
    return render_template("index.html", title = "Namaste", posts = posts, form=form)

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

@app.before_request
def before_request():
    if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

@app.route("/edit_profile" , methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form = form)


@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User {} not found.".format(username))
        return redirect(url_for("index"))
    if user == current_user:
        flash("You cannot follow yourself!")
        return redirect(url_for("user", username=username))
    current_user.follow(user)
    db.session.commit()
    flash("You are follwing {}!".format(username))
    return redirect(url_for("user", username=username))


@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User {} not found.".format(username))
        return redirect(url_for("index"))
    if user == current_user:
        flash( "You cannot unfollow yourself!")
    current_user.unfollow(user)
    db.session.commit()
    flash("You unfollowed {}!". format(username))
    return redirect(url_for("user",username=username))


@app.route("/explore")
@login_required
def explore()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", posts=posts)