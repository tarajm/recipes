from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users_models import User
from flask import flash


db = 'recipes'
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.posted_by = None

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True # we assume this is true
        if len(recipe['name']) < 2:
            flash("Name must be at least 2 characters.", "name")
            is_valid = False
        if len(recipe['description']) < 2:
            flash("Description must be at least 2 characters.", "description")
            is_valid = False
        if len(recipe['instructions']) < 2:
            flash("Instructions must be at least 2 characters.", "instructions")
            is_valid = False
        if len(recipe['under_30']) == 0:
            flash("Under 30 must not be left blank.", "under_30")
            is_valid = False
        return is_valid

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * from recipes JOIN users on users.id = recipes.users_id;"
        results = connectToMySQL(db).query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipe.posted_by = User(
                {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
                }
            )
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def add_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, users_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(users_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    # @classmethod
    # def get_one_recipe(cls, data):
    #     query = "SELECT * FROM recipes WHERE id = %(id)s;"
    #     results = connectToMySQL(db).query_db(query, data)
    #     return cls(results[0])

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.users_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        recipe = cls(results[0])
        recipe.posted_by = results[0]['first_name']
        return recipe

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET  name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)