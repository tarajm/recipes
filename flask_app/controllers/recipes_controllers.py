from flask import render_template,redirect,request,session
from flask import flash
from flask_app import app
from flask_app.models.recipes_models import Recipe
from flask_app.controllers import users_controllers

@app.route('/create', methods=['POST'])
def create_recipe():
    if 'users_id' not in session:
        return redirect('/')
    # if 'under_30' not in request.form.keys():
    #     unchecked = 'unchecked'
    # else:
    #     unchecked = request.form['under_30']
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30'],
        'users_id': session['users_id']
    }
    if not Recipe.validate_recipe(data):
        return redirect('/recipe/new')
    Recipe.add_recipe(data)
    return redirect('/recipes')

@app.route('/delete/<int:id>')
def delete(id):
    if 'users_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Recipe.delete(data)
    return redirect('/recipes')

@app.route('/edit/<int:id>')
def edit(id):
    if 'users_id' not in session:
        return redirect('/')
    data = {
        'id':id
    }
    return render_template('edit.html', recipe = Recipe.get_one_recipe(data))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'users_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'id': id
    }
    Recipe.update(request.form)
    return redirect('/recipes')

@app.route('/view/<int:id>')
def show_recipe(id):
    if 'users_id' not in session:
        return redirect('/')
    data = {
        'id':id
    }
    recipe = Recipe.get_one_recipe(data)
    return render_template('view.html', recipe = recipe)