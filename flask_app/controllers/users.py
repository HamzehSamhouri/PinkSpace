from flask_app import app, render_template, redirect, request, bcrypt, session, flash

from flask_app.models.user import User
from flask_app.models.friendship import Friendship


import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "flask_app/static/img"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# MAIN LOGIN/REGISTER PAGE
@app.route("/")
def index():
    return render_template("index.html")


#! REGISTER
@app.route("/register", methods=["post"])
def register():
    if not User.validate_user(request.form):  # USER VALIDATION staticmethod
        return redirect("/")

    hashed_password = bcrypt.generate_password_hash(request.form["password"])
    print(hashed_password)  # GENERATE HASHED PASSWORD

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_password,
        "filename": "newuser.png" 
    }

    user_id = User.save(data)
    session["user_id"] = user_id
    session["first_name"] = request.form["first_name"]
    session["last_name"] = request.form["last_name"]
    session["email"] = request.form["email"]

    return redirect("/homepage")


#! LOGIN: READ AND VERIFY
@app.route("/login", methods=["post"])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password", "login")
        return redirect("/")

    session["user_id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    session["last_name"] = user_in_db.last_name

    return redirect("/homepage")


@app.route("/friendship/create", methods=["POST"])
def add_friend():
    Friendship.save(request.form)
    return redirect(f"/friends/{request.form['user_id']}")


# Friends
@app.route("/friends/<int:id>")
def friends(id):
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    return render_template(
        "friends.html", friends=User.get_friends({"id": id}), users=User.get_all()
    )  # GET_ALL_FRIENDS and GET_ALL USERS classmethod


# DELETE USER
@app.route("/user/delete/<int:id>")
def delete_user(id):
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    data = {"id": id}
    User.delete(data)  # DELETE classmethod
    return redirect("/")


# DELETE FRIENDSHIP
@app.route("/friendship/delete/<int:id>/<int:return_to>")
def remove_friend(id, return_to):
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    data = {"id": id}
    Friendship.delete(data)  # DELETE classmethod
    return redirect(f"/friends/{return_to}")


# EDIT USER
@app.route("/edit/user/<int:id>")
def edit_profile(id):
    data = {"id": id}
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    return render_template("edit_profile.html", user=User.get_one_user(data))

# USER UPDATE AND FILE UPLOAD
@app.route("/user/update/<int:id>", methods=["POST"])
def update_user(id):
    print(request.form)
    # check if the post request has a file part
    if "file" not in request.files:
        print("No file part")
        return redirect(f"/edit/user/{id}")

    # if file part exists in form, save to variable
    file = request.files["file"]

    # if the user does not select a file, browser submits an empty part without filename
    if file.filename == "":
        print("No selected file")
        return redirect(f"/edit/user/{id}")

    # if valid file submitted, save into local folder (does *NOT* save in database!)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

    # saves the image into the static/img folder
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    # saves img filename in SQL db for reference
    # new_file_id = User.save({"filename": filename})
    file_data = {
        **request.form,
        'filename' : filename
    }

    if not User.validate_update(file_data): 

    # USER VALIDATION staticmethod
        return redirect(f"/edit/user/{id}")

    User.update(file_data)
    return redirect(f"/user/{id}")
