from flask_app import app, render_template, redirect, session, request
from flask_app.models.comment import Comment
from flask_app.models.user import User 


# CREATE COMMENT
@app.route('/comment/create', methods = ['POST'])
def create_comment():
    if 'user_id' not in session:
        return redirect('/logout') #User must be logged in to view the dashboard
    if not Comment.validate_comment(request.form):
        return redirect('/homepage')  #VALIDATION staticmethod
    Comment.save(request.form) #SAVE classmethod
    return redirect('/homepage')


# CREATE COMMENT ON PROFILE
@app.route('/comment/create/profile/<int:return_to>', methods = ['POST'])
def create_comment_profile(return_to):
    if 'user_id' not in session:
        return redirect('/logout') #User must be logged in to view the dashboard
    if not Comment.validate_comment(request.form):
            return redirect(f"/user/{return_to}")#VALIDATION staticmethod
    Comment.save(request.form) #SAVE classmethod
    return redirect(f"/user/{return_to}")


# DELETE COMMENT
@app.route('/comment/delete/<int:id>')
def delete_comment(id):
    if 'user_id' not in session:
        return redirect('/logout') #User must be logged in to view the dashboard
    data ={'id': id}
    Comment.delete(data) #DELETE classmethod
    return redirect('/homepage')


# DELETE COMMENT ON PROFILE
@app.route('/comment/delete/profile/<int:id>/<int:return_to>')
def delete_comment_profile(id, return_to):
    if 'user_id' not in session:
        return redirect('/logout') #User must be logged in to view the dashboard
    data ={'id': id}
    Comment.delete(data) #DELETE classmethod
    return redirect(f"/user/{return_to}")