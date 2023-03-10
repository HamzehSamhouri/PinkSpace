from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, session

DATABASE = 'myspace'


class Friendship:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.created_at = data['created_at']
        self.user_id = data['user_id']
        self.friendship_id = data['friendship_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.filename = data['filename']


# ADD NEW FRIEND
    @classmethod
    def save(cls, data):
        query = "INSERT IGNORE INTO friendships (user_id, friend_id) VALUES (%(user_id)s, %(friend_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


# DELETE FRIEND
    @classmethod
    def delete(cls,data):
            query  = "DELETE FROM friendships WHERE id = %(id)s;"
            return connectToMySQL(DATABASE).query_db(query,data)