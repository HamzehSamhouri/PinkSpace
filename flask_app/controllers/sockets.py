from flask_app import app, Flask, render_template, redirect, session

from flask_socketio import SocketIO

from flask_app.models.user import User

socketio = SocketIO(app, manage_session=False)

# Page Render
@app.route("/chat")
def testchat():
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the profile
    return render_template(
        "chat.html", users=User.get_all())  # GET_ALL USERS classmethod


def messageReceived(methods=["GET", "POST"]):
    print("Message received,")


@socketio.on("my event")
def handle_my_custom_event(json, methods=["GET", "POST"]):
    print("received my event: " + str(json))
    socketio.emit("my response", json, callback=messageReceived)
