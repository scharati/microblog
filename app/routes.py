from app import app
from flask import render_template

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