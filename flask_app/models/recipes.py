from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import users
from flask import flash
from flask_bcrypt import Bcrypt
import re

class Recipe:
    db = "recipes_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user_first_name = data['first_name']
    
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def get_recipe_by_id(cls,id):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        data = {
            "id": id
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s, updated_at = NOW() WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        data = {
            "id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return result
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("First Name must be at least 3 characters.", 'recipe')
            is_valid = False
        if len(data['description']) < 2:
            flash("Description must be at least 3 characters.", 'recipe')
            is_valid = False
        if len(data['instructions']) < 2:
            flash("Instructions must be at least 3 characters.", 'recipe')
            is_valid = False
        if not data['date_made']:
            flash("Please include date made.", 'recipe')
            is_valid = False
        if not data['under_30']:
            flash("Please specify if recipe takes under 30 minutes.", 'recipe')
            is_valid = False
        return is_valid