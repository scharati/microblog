from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
    return render_template("index.html", user = user, title = "Namaste", posts = posts)

@app.route('/login' , methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash( 'Login requested for user {}, remember_me={}'.format( form.username.data, form.remember_me.data ) )
        return redirect( url_for("index") )
    else:
        return render_template('login.html', title='Sign In', form = form)