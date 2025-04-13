from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.CategorieController import CategorieController

categorie_routes = Blueprint('categorie', __name__, url_prefix='/categories')


@categorie_routes.route('/')
def index():
    categories = CategorieController.read_all()
    return render_template('categories/index.html', categories=categories)


@categorie_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'nom': request.form['nom']
        }
        success, result = CategorieController.create(data)
        if success:
            return redirect(url_for('categorie.index'))
        return render_template('categories/create.html', error=result)

    return render_template('categories/create.html')


@categorie_routes.route('/update/<int:categorie_id>', methods=['GET', 'POST'])
def update(categorie_id):
    categorie = CategorieController.read_one(categorie_id)
    if not categorie:
        return redirect(url_for('categorie.index'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom']
        }
        success, result = CategorieController.update(categorie_id, data)
        if success:
            return redirect(url_for('categorie.index'))
        return render_template('categories/update.html', categorie=categorie, error=result)

    return render_template('categories/update.html', categorie=categorie)


@categorie_routes.route('/delete/<int:categorie_id>', methods=['POST'])
def delete(categorie_id):
    success, result = CategorieController.delete(categorie_id)
    return redirect(url_for('categorie.index'))
