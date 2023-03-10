from flask_app import app, render_template, redirect, session, request
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.comment import Comment

import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = "flask_app/static/img"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# HOMEPAGE
@app.route("/homepage")
def posts():
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    return render_template(
        "homepage.html", posts=Post.get_posts_with_comments()
    )  # GET_ALL_POSTS classmethod


# PROFILE POSTS
@app.route("/user/<int:id>")
def posts_by_id(id):
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the profile
    return render_template(
        "profile.html",
        user=User.get_one_user({"id": id}),
        posts=Post.get_posts_by_id({"id": id}),
    )  # GET_POSTS_BY_ID classmethod


# NEW POST
@app.route("/post/create", methods=["POST"])
def create_post():
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    if not Post.validate_post(request.form):
        return redirect("/homepage")  # VALIDATION staticmethod
        # check if the post request has a file part
    Post.save(request.form)  # SAVE classmethod
    return redirect("/homepage")


# NEW POST ON PROFILE
@app.route("/post/create/profile", methods=["POST"])
def create_post_profile():
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    if not Post.validate_post(request.form):
        return redirect(f"/user/{request.form['user_id']}")  # VALIDATION staticmethod
    Post.save(request.form)  # SAVE classmethod
    return redirect(f"/user/{request.form['user_id']}")


# DELETE POST
@app.route("/post/delete/<int:id>")
def delete_post(id):
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    data = {"id": id}
    Post.delete(data)  # DELETE classmethod
    return redirect("/homepage")


# DELETE POST ON PROFILE
@app.route("/post/delete/profile/<int:id>/<int:return_to>")
def delete_post_profile(id, return_to):
    if "user_id" not in session:
        return redirect("/logout")  # User must be logged in to view the dashboard
    data = {"id": id}
    Post.delete(data)  # DELETE classmethod
    return redirect(f"/user/{return_to}")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# # CHAT TEST
# @app.route("/test")
# def chat():
#     if "user_id" not in session:
#         return redirect("/logout")  # User must be logged in to view the dashboard
#     return render_template("testchat.html")