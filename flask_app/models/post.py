from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app import flash
from flask_app.models import comment


# DATABASE VARIABLE LINKING TO MYSQL
DATABASE = 'myspace';

# POST CLASS
class Post:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        # TO LINK CORRESPONDING USER DATA
        self.user_id = data['user_id']
        self.filename = data['filename']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        # ADD COMMENTS
        self.comments = []



# SAVE POST
    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)



# GET ALL POSTS WITH COMMENTS
    @classmethod
    def get_posts_with_comments (cls):
        query = """
        SELECT * FROM posts LEFT JOIN users posters ON posts.user_id = posters.id LEFT JOIN comments ON posts.id = comments.post_id LEFT JOIN users commenters ON comments.user_id = commenters.id ORDER BY posts.created_at DESC; 
        """
        results = connectToMySQL(DATABASE).query_db(query)
        posts = []
        post_ids = []

        for row in results:
            if row['id'] not in post_ids:
                post_ids.append(row['id'])
                posts.append(cls(row))
            if row['comments.id']:
                comment_data = {
                    'id' : row['comments.id'],
                    'content' : row['comments.content'],
                    'created_at' : row['created_at'],

                    # TO LINK CORRESPONDING USER
                    'user_id' : row['commenters.id'],
                    'first_name' : row['commenters.first_name'],
                    'last_name' : row['commenters.last_name'],

                    # TO LINK CORRESPONDING POST
                    'post_id' : row['post_id']

                }
                new_comment = comment.Comment(comment_data)
                last_post = posts[len(posts) - 1]
                last_post.comments.append(new_comment)

        return posts


# GET ALL POSTS BY SPECIFIC USER
    @classmethod
    def get_posts_by_id (cls, data):
        query = """
        SELECT * FROM posts LEFT JOIN users posters ON posts.user_id = posters.id LEFT JOIN comments ON posts.id = comments.post_id LEFT JOIN users commenters ON comments.user_id = commenters.id WHERE posters.id = %(id)s ORDER BY posts.created_at DESC; 
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        posts = []
        post_ids = []

        for row in results:
            if row['id'] not in post_ids:
                post_ids.append(row['id'])
                posts.append(cls(row))
            if row['comments.id']:
                comment_data = {
                    'id' : row['comments.id'],
                    'content' : row['comments.content'],
                    'created_at' : row['created_at'],

                    # TO LINK CORRESPONDING USER
                    'user_id' : row['commenters.id'],
                    'first_name' : row['commenters.first_name'],
                    'last_name' : row['commenters.last_name'],

                    # TO LINK CORRESPONDING POST
                    'post_id' : row['post_id']

                }
                new_comment = comment.Comment(comment_data)
                last_post = posts[len(posts) - 1]
                last_post.comments.append(new_comment)

        return posts


# DELETE POST
    @classmethod
    def delete(cls,data):
            query  = "DELETE FROM posts WHERE id = %(id)s;"
            return connectToMySQL(DATABASE).query_db(query,data)


# VALIDATE POST
    @staticmethod
    def validate_post(post):

        is_valid = True

        if len(post['content']) < 1:
            is_valid = False
            flash("Post must not be blank", "post")

        return is_valid