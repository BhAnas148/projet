from src.controllers.ImageController import ImageController  # Add this import
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.CategorieController import CategorieController
from src.controllers.SousCategorieController import SousCategorieController
from src.controllers.ProduitController import ProduitController

produit_routes = Blueprint('produit', __name__, url_prefix='/produits')

# Configuration for file uploads
UPLOAD_FOLDER = 'static/produits/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@produit_routes.route('/')
def index():
    produits = ProduitController.read_all()
    return render_template('produits/index.html', produits=produits)


@produit_routes.route('/details/<int:produit_id>')
def details(produit_id):
    # Get the product
    produit = ProduitController.read_one(produit_id)
    if not produit:
        return redirect(url_for('produit.index'))

    # Get all images for this product
    images = ImageController.read_all(produit_id)

    # Get the product's category and subcategory
    categorie = CategorieController.read_one(produit.categorie_id)
    sous_categorie = SousCategorieController.read_one(
        produit.sous_categorie_id)

    return render_template('produits/details.html',
                           produit=produit,
                           images=images,
                           categorie=categorie,
                           sous_categorie=sous_categorie)


@produit_routes.route('/create', methods=['GET', 'POST'])
def create():
    categories = CategorieController.read_all()
    sous_categories = SousCategorieController.read_all()

    if request.method == 'POST':
        data = {
            'designation': request.form['designation'],
            'description': request.form['description'],
            'prix_vente': request.form['prix_vente'],
            'categorie_id': request.form['categorie_id'],
            'sous_categorie_id': request.form['sous_categorie_id']
        }

        # Handle file upload
        if 'image' not in request.files:
            return render_template('produits/create.html',
                                   error='No file part',
                                   categories=categories,
                                   sous_categories=sous_categories)

        file = request.files['image']

        if file.filename == '':
            return render_template('produits/create.html',
                                   error='No selected file',
                                   categories=categories,
                                   sous_categories=sous_categories)

        if file and allowed_file(file.filename):
            # Secure the filename and ensure directory exists
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # Save the file
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Add file info to data
            data['image_nom'] = filename
            data['is_primary'] = True

        success, result = ProduitController.create(data)
        if success:
            return redirect(url_for('produit.index'))
        return render_template('produits/create.html',
                               error=result,
                               categories=categories,
                               sous_categories=sous_categories)

    return render_template('produits/create.html',
                           categories=categories,
                           sous_categories=sous_categories)


@produit_routes.route('/update/<int:produit_id>', methods=['GET', 'POST'])
def update(produit_id):
    produit = ProduitController.read_one(produit_id)
    if not produit:
        return redirect(url_for('produit.index'))

    categories = CategorieController.read_all()
    sous_categories = SousCategorieController.read_all()

    if request.method == 'POST':
        data = {
            'designation': request.form['designation'],
            'description': request.form['description'],
            'prix_vente': request.form['prix_vente'],
            'categorie_id': request.form['categorie_id'],
            'sous_categorie_id': request.form['sous_categorie_id']
        }

        # Handle file upload if a new file was provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                # Remove old file if exists
                if produit.image_nom and produit.image_nom != 'default.jpg':
                    old_file = os.path.join(UPLOAD_FOLDER, produit.image_nom)
                    if os.path.exists(old_file):
                        os.remove(old_file)

                # Save new file
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                data['image_nom'] = filename

        success, result = ProduitController.update(produit_id, data)
        if success:
            return redirect(url_for('produit.index'))
        return render_template('produits/update.html',
                               produit=produit,
                               error=result,
                               categories=categories,
                               sous_categories=sous_categories)

    return render_template('produits/update.html',
                           produit=produit,
                           categories=categories,
                           sous_categories=sous_categories)


@produit_routes.route('/delete/<int:produit_id>', methods=['POST'])
def delete(produit_id):
    # Optional: Delete associated image file when deleting product
    produit = ProduitController.read_one(produit_id)
    if not produit:
        return redirect(url_for('produit.index'))

    success, result = ProduitController.delete(produit_id)
    return redirect(url_for('produit.index'))
