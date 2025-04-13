from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.CategorieController import CategorieController
from src.controllers.SousCategorieController import SousCategorieController

sous_categorie_routes = Blueprint(
    'sous_categorie', __name__, url_prefix='/sous-categories')


@sous_categorie_routes.route('/')
def index():
    sous_categories = SousCategorieController.read_all()
    return render_template('sous_categories/index.html', sous_categories=sous_categories)


@sous_categorie_routes.route('/create', methods=['GET', 'POST'])
def create():
    categories = CategorieController.read_all()  # Fetch categories for dropdown
    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'categorie_id': request.form['categorie_id']
        }
        success, result = SousCategorieController.create(data)
        if success:
            return redirect(url_for('sous_categorie.index'))  # Use singular 'sous_categorie.index'
        return render_template('sous_categories/create.html', error=result, categories=categories)

    return render_template('sous_categories/create.html', categories=categories)


@sous_categorie_routes.route('/update/<int:sous_categorie_id>', methods=['GET', 'POST'])
def update(sous_categorie_id):
    sous_categorie = SousCategorieController.read_one(sous_categorie_id)
    if not sous_categorie:
        return redirect(url_for('sous_categorie.index'))  # Use singular 'sous_categorie.index'

    categories = CategorieController.read_all()  # Fetch categories for dropdown

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'categorie_id': request.form['categorie_id']
        }
        success, result = SousCategorieController.update(
            sous_categorie_id, data)
        if success:
            return redirect(url_for('sous_categorie.index'))  # Use singular 'sous_categorie.index'
        return render_template('sous_categories/update.html', sous_categorie=sous_categorie, error=result, categories=categories)

    return render_template('sous_categories/update.html', sous_categorie=sous_categorie, categories=categories)


@sous_categorie_routes.route('/delete/<int:sous_categorie_id>', methods=['POST'])
def delete(sous_categorie_id):
    success, result = SousCategorieController.delete(sous_categorie_id)
    return redirect(url_for('sous_categorie.index'))  # Use singular 'sous_categorie.index'
