from app import app
from Flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {"username" : 'Shailesh'}
    return """
    <html>
        <head>
            <title>Home Page - Microblog </title>
        </head>
        <body>
            <h1>Namaste,""" + user["username"]+"""!</h1>
        </body>
    </html>
    """