import os

from flask import Blueprint, render_template, request, redirect, url_for
#from flask_uploads import UploadSet, configure_uploads, IMAGES

from src.controllers.CategorieController import CategorieController
from src.controllers.SousCategorieController import SousCategorieController
from src.controllers.ProduitController import ProduitController

produit_routes = Blueprint(
    'produit', __name__, url_prefix='/produits')

# Setup file upload
# photos = UploadSet("photos", IMAGES)
# produit_routes.config['UPLOADED_PHOTOS_DEST'] = 'static/produits/'
# configure_uploads(produit_routes, photos)


@produit_routes.route('/')
def index():
    produits = ProduitController.read_all()
    return render_template('produits/index.html', produits=produits)


@produit_routes.route('/create', methods=['GET', 'POST'])
def create():
    categories = CategorieController.read_all()  # Get all categories
    sous_categories = SousCategorieController.read_all()  # Get all sous-categories

    if request.method == 'POST':
        data = {
            'designation': request.form['designation'],
            'description': request.form['description'],
            'prix_vente': request.form['prix_vente'],
            'categorie_id': request.form['categorie_id'],
            'sous_categorie_id': request.form['sous_categorie_id']
        }

        # Handle file upload for image
        # file = request.files['image']
        # if file:
        #     filename = photos.save(file)
        #     data['image_nom'] = filename
        #     data['is_primary'] = True  # Mark the image as primary

        success, result = ProduitController.create(data)
        if success:
            return redirect(url_for('produit.index'))
        return render_template('produits/create.html', error=result, categories=categories, sous_categories=sous_categories)

    return render_template('produits/create.html', categories=categories, sous_categories=sous_categories)


@produit_routes.route('/update/<int:produit_id>', methods=['GET', 'POST'])
def update(produit_id):
    produit = ProduitController.read_one(produit_id)
    if not produit:
        return redirect(url_for('produit.index'))

    categories = CategorieController.read_all()  # Get all categories
    sous_categories = SousCategorieController.read_all()  # Get all sous-categories

    if request.method == 'POST':
        data = {
            'designation': request.form['designation'],
            'description': request.form['description'],
            'prix_vente': request.form['prix_vente'],
            'categorie_id': request.form['categorie_id'],
            'sous_categorie_id': request.form['sous_categorie_id']
        }

        # Handle file upload for image (optional, only if user uploads a new one)
        # file = request.files['image']
        # if file:
        #     filename = photos.save(file)
        #     data['image_filename'] = filename

        data['image_filename'] = "default.jpg"
        success, result = ProduitController.update(produit_id, data)
        if success:
            return redirect(url_for('produit.index'))
        return render_template('produits/update.html', produit=produit, error=result, categories=categories, sous_categories=sous_categories)

    return render_template('produits/update.html', produit=produit, categories=categories, sous_categories=sous_categories)


@produit_routes.route('/delete/<int:produit_id>', methods=['POST'])
def delete(produit_id):
    success, result = ProduitController.delete(produit_id)
    return redirect(url_for('produit.index'))
