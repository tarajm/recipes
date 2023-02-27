from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'recipes'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'first_name')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", 'email')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'password')
            is_valid = False
        if not re.search("[A-Z]", user['password']):
            flash("Password must contain at least one capital letter.", 'password')
        if not re.search("[0-9]", user['password']):
            flash("Password must contain at least one number.", 'password')
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", 'confirm_password')
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s )"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        # didnt find a matching user
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    
