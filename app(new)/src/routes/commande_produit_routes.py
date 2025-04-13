from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.CommandeProduitController import CommandeProduitController

commande_produit_routes = Blueprint(
    'commande_produit', __name__, url_prefix='/commande_produits')


@commande_produit_routes.route('/<int:commande_id>/add', methods=['GET', 'POST'])
def add_to_command(commande_id):
    if request.method == 'POST':
        data = {
            'commande_id': commande_id,
            'produit_id': request.form['produit_id'],
            'prix_unitaire': request.form['prix_unitaire'],
            'quantite': request.form['quantite']
        }
        success, result = CommandeProduitController.add_to_command(data)
        if success:
            return redirect(url_for('commandes.read_one', commande_id=commande_id))
        return render_template('commande_produits/add.html', error=result)

    return render_template('commande_produits/add.html', commande_id=commande_id)


@commande_produit_routes.route('/<int:commande_produit_id>/update', methods=['GET', 'POST'])
def update(commande_produit_id):
    commande_produit = CommandeProduitController.read_one(commande_produit_id)
    if not commande_produit:
        return redirect(url_for('commandes.index'))

    if request.method == 'POST':
        data = {
            'quantite': request.form['quantite'],
            'prix_unitaire': request.form['prix_unitaire']
        }
        success, result = CommandeProduitController.update(
            commande_produit_id, data)
        if success:
            return redirect(url_for('commandes.read_one', commande_id=commande_produit.commande_id))
        return render_template('commande_produits/update.html', error=result, commande_produit=commande_produit)

    return render_template('commande_produits/update.html', commande_produit=commande_produit)


@commande_produit_routes.route('/<int:commande_produit_id>/delete', methods=['POST'])
def delete(commande_produit_id):
    success, result = CommandeProduitController.delete(commande_produit_id)
    if success:
        return redirect(url_for('command.read_one', commande_id=commande_produit_id))
    return redirect(url_for('command.index'))  # Handle error if necessary
