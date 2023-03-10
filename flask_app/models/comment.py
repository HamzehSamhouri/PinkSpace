from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models import post
from flask_app import flash



# DATABASE VARIABLE LINKING TO MYSQL
DATABASE = 'myspace';


# COMMENT CLASS
class Comment:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']

        # TO LINK CORRESPONDING USER
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']

        # TO LINK CORRESPONDING POST
        self.post_id = data['post_id']



# SAVE COMMENT
    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (content, user_id, post_id) VALUES (%(content)s, %(user_id)s, %(post_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)


# DELETE COMMENT
    @classmethod
    def delete(cls,data):
            query  = "DELETE FROM comments WHERE id = %(id)s;"
            return connectToMySQL(DATABASE).query_db(query,data)



# VALIDATE COMMENT
    @staticmethod
    def validate_comment(comment):
        is_valid = True

        if len(comment['content']) < 1:
            is_valid = False
            flash("Comment must not be blank", "comment")

        return is_valid