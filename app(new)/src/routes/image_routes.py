import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from datetime import datetime
from werkzeug.utils import secure_filename

from src.controllers.ImageController import ImageController

# Blueprint setup
image_routes = Blueprint('produit_images', __name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/produits/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_routes.route("/produits/<int:produit_id>/images/create", methods=["GET", "POST"])
def images_create(produit_id):
    if request.method == "POST":
        is_primary = request.form.get("is_primary", "off") == "on"

        # Handle file upload
        if 'image' not in request.files:
            flash('Aucun fichier sélectionné', 'danger')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Secure the filename and ensure directory exists
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Save the file
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Create image record
            ImageController.create(produit_id, filename, is_primary)
            
            # If set as primary, update selection
            if is_primary:
                images = ImageController.read_all(produit_id)
                if images:
                    ImageController.update_selection(produit_id, images[-1].id)

            flash("Image ajoutée avec succès", "success")
            return redirect(url_for("produit.details", produit_id=produit_id))
        else:
            flash("Type de fichier non autorisé", "danger")

    return render_template("produits/images/create.html", produit_id=produit_id)

@image_routes.route("/produits/<int:produit_id>/images/update/<int:image_id>", methods=["GET", "POST"])
def images_update(produit_id, image_id):
    image = ImageController.read_one(image_id)
    if not image:
        flash("Image non trouvée", "danger")
        return redirect(url_for("produit.details", produit_id=produit_id))

    if request.method == "POST":
        is_primary = request.form.get("is_primary", "off") == "on"

        # Handle file upload if new file provided
        filename = image.nom
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                # Remove old file if exists
                if image.nom and image.nom != 'default.jpg':
                    old_file = os.path.join(UPLOAD_FOLDER, image.nom)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                
                # Save new file
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Update image record
        ImageController.update(image_id, filename=filename, is_primary=is_primary)
        
        # If set as primary, update selection
        if is_primary:
            ImageController.update_selection(produit_id, image_id)

        flash("Image modifiée avec succès", "success")
        return redirect(url_for("produit.details", produit_id=produit_id))

    return render_template("produits/images/update.html", 
                         image=image, 
                         produit_id=produit_id)

@image_routes.route("/produits/<int:produit_id>/images/delete/<int:image_id>", methods=["GET"])
def images_delete(produit_id, image_id):
    images = ImageController.read_all(produit_id)
    if len(images) <= 1:
        flash("Le produit doit avoir au moins une image", "danger")
        return redirect(url_for("produit.details", produit_id=produit_id))

    image = ImageController.read_one(image_id)
    if image:
        # Delete file if exists
        if image.nom and image.nom != 'default.jpg':
            file_path = os.path.join(UPLOAD_FOLDER, image.nom)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete record
        ImageController.delete(image_id)
        
        # If deleting primary, set a new primary
        if image.is_primary:
            remaining_images = ImageController.read_all(produit_id)
            if remaining_images:
                ImageController.update_selection(produit_id, remaining_images[0].id)

        flash("Image supprimée avec succès", "success")
    else:
        flash("Image non trouvée", "danger")

    return redirect(url_for("produit.details", produit_id=produit_id))

@image_routes.route("/produits/<int:produit_id>/images/set-primary/<int:image_id>", methods=["GET"])
def set_primary_image(produit_id, image_id):
    success, result = ImageController.set_primary(produit_id, image_id)
    if success:
        flash("Image principale mise à jour", "success")
    else:
        flash(result, "danger")
    return redirect(url_for("produit.details", produit_id=produit_id))