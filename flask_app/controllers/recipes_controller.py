from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import recipes
from flask_app.controllers import users_controller

@app.route('/recipes')
def success():
    if "user_id" in session:
        all_recipes = recipes.Recipe.get_all_recipes()
        return render_template("dashboard.html", all_recipes=all_recipes)
    else:
        return redirect('/')
    
@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    if "user_id" in session:
        recipe = recipes.Recipe.get_recipe_by_id(recipe_id)
        return render_template("show_recipe.html", recipe=recipe)
    else:
        return redirect('/')
    
@app.route('/recipes/new')
def new_recipe():
    if "user_id" in session:
        return render_template("new_recipe.html")
    else:
        return redirect('/')

@app.route('/recipes/save', methods=["POST"])
def create_recipe():
    print(request.form["under_30"])
    if "user_id" in session:
        data = {
            "name": request.form["recipe_name"],
            "description": request.form["recipe_description"],
            "instructions": request.form["recipe_instructions"],
            "date_made": request.form["date_made"],
            "under_30": request.form["under_30"],
            "user_id": session["user_id"]
        }
        if not recipes.Recipe.validate_recipe(data):
            session['recipe_name'] = request.form['recipe_name']
            session['description'] = request.form['recipe_description']
            session['instructions'] = request.form['recipe_instructions']
            session['date_made'] = request.form['date_made']
            return redirect('/recipes/new')
        recipes.Recipe.save_recipe(data)
        session.pop("recipe_name")
        return redirect('/recipes')
    else:
        return redirect('/')

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if "user_id" in session:
        recipe = recipes.Recipe.get_recipe_by_id(recipe_id)
        return render_template("edit_recipe.html", recipe=recipe)
    else:
        return redirect('/')

@app.route('/recipes/update/<int:recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    if "user_id" in session:
        data = {
            "name": request.form["recipe_name"],
            "description": request.form["recipe_description"],
            "instructions": request.form["recipe_instructions"],
            "date_made": request.form["date_made"],
            "under_30": request.form["under_30"],
            "id": recipe_id
        }
        if not recipes.Recipe.validate_recipe(data):
            session['recipe_name'] = request.form['recipe_name']
            session['description'] = request.form['recipe_description']
            session['instructions'] = request.form['recipe_instructions']
            session['date_made'] = request.form['date_made']
            return redirect(f"/recipes/edit/{recipe_id}")
        recipes.Recipe.update_recipe(data)
        return redirect(f"/recipes")
    else:
        return redirect('/')

@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if "user_id" in session:
        print(recipe_id)
        recipes.Recipe.delete_recipe(recipe_id)
        return redirect('/recipes')
    else:
        return redirect('/')
