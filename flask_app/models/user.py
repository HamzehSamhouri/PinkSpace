from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models.friendship import Friendship

# REGEX MODEL
import re

# EMAIL FORMAT
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# PASSWORD FORMAT
PASSWORD_REGEX = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")


# DATABASE VARIABLE LINKING TO MYSQL
DATABASE = 'myspace'


class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.filename = data['filename']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.friends = []


# SAVE USER REGISTER DATA
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (filename, first_name, last_name, email, password, created_at, updated_at) VALUES (%(filename)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)



# CHECK IF EMAIL EXISTS IN DATABASE (to login)
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


# GET ALL USERS' DATA
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users



# GET ONE USERS' DATA
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users where users.id = %(id)s ;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])


# UPDATE A USER
    @classmethod
    def update(cls,data):
        print(data)
        query = "UPDATE users SET filename=%(filename)s, first_name=%(first_name)s, last_name=%(last_name)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)



# GET ALL USERS' FRIENDS
    @classmethod
    def get_friends(cls, data):
        query = """
        Select * FROM users LEFT JOIN friendships ON users.id = friendships.user_id LEFT JOIN users friends ON friends.id = friendships.friend_id WHERE users.id = %(id)s;"""

        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        friendships = []
        for row in results:
            friend_data = {
                'id' : row['friends.id'],
                'first_name' : row['friends.first_name'],
                'last_name' : row['friends.last_name'],
                'filename' : row['friends.filename'],
                'friendship_id' : row['friendships.id'],
                'user_id' : row['user_id'],
                'created_at' : row['created_at']
            }

            friendships.append(Friendship(friend_data))
        return friendships



# DELETE USER
    @classmethod
    def delete(cls,data):
            query  = "DELETE FROM users WHERE id = %(id)s;"
            return connectToMySQL(DATABASE).query_db(query,data)



# VALIDATE USER REGISTRATION
    @staticmethod
    def validate_user(user:dict) -> bool:

        is_valid = True

    # USED TO CHECK IF EMAIL IS ALREADY IN DATABASE 
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,user)

    # FIRST NAME
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First Name must be at least 2 characters", "reg")

    # LAST NAME
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last Name must be at least 2 characters", "reg")

    # EMAIL
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid Email Address", "reg")
            is_valid = False

    # EMAIL ALREADY TAKEN?
        if len(results) >= 1:
            flash("Email already taken","reg")
            is_valid=False

    # PASSWORD
        if not PASSWORD_REGEX.match(user['password']): 
            flash("Invalid Password", "reg")
            is_valid = False
    
    # DO PASSWORDS MATCH?
        if user['password'] !=  user['confirm-password'] :
            is_valid = False
            flash("Passwords do NOT match", "reg")

        return is_valid



# VALIDATE USER UPDATE
    @staticmethod
    def validate_update(user:dict) -> bool:

        is_valid = True

    # FIRST NAME
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First Name must be at least 2 characters", "update")

    # LAST NAME
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last Name must be at least 2 characters", "update")

        return is_valid