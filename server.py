from flask_app import app
from flask_app.controllers import users, posts, comments, sockets

if __name__ == '__main__':
    app.run(debug=True)