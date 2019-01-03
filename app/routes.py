from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {"username" : 'Shailesh'}
    return render_template("index.html", user = user, title = "Namaste")