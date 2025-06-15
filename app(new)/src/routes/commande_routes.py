from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.controllers.UserController import UserController
from src.controllers.CommandeController import CommandeController
from src.controllers.CommandeProduitController import CommandeProduitController
from src.controllers.ProduitController import ProduitController

# Blueprint name is 'commandes' (plural)
commande_routes = Blueprint('commandes', __name__, url_prefix='/commandes')

@commande_routes.route('/')
def index():
    commandes = CommandeController.read_all()
    return render_template('commandes/index.html', commandes=commandes)

@commande_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'client_id': request.form['client_id'],
            'montant_total': 0,
            'nb_article': 0,
        }
        success, result = CommandeController.create(data)
       
        if success:
            flash('Commande créée avec succès.', 'success')
            return redirect(url_for('commandes.read_one', commande_id=result.id))
        return render_template('commandes/create.html', error=result)

    clients = UserController.get_users_by_role('client')
    return render_template('commandes/create.html', clients=clients)

@commande_routes.route('/details/<int:commande_id>')
def read_one(commande_id):
    commande = CommandeController.read_one(commande_id)
    if commande:
        produits = CommandeProduitController.read_all(commande_id)
        nb_article = sum(p.quantite for p in produits)
        montant_total = sum(p.prix_total for p in produits)
        return render_template('commandes/details.html', commande=commande, produits=produits, nb_article=nb_article, montant_total=montant_total)
    return redirect(url_for('commandes.index'))

@commande_routes.route('/update/<int:commande_id>', methods=['GET', 'POST'])
def update(commande_id):
    commande = CommandeController.read_one(commande_id)
    if not commande:
        return redirect(url_for('commandes.index'))

    if request.method == 'POST':
        data = {
            'client_id': request.form['client_id'],
            'montant_total': request.form['montant_total'],
            'nb_article': request.form['nb_article']
        }
        success, result = CommandeController.update(commande_id, data)
        if success:
            return redirect(url_for('commandes.read_one', commande_id=commande_id))
        return render_template('commandes/update.html', error=result, commande=commande)

    return render_template('commandes/update.html', commande=commande)

@commande_routes.route('/delete/<int:commande_id>')
def delete(commande_id):
    success, result = CommandeController.delete(commande_id)
    if success:
        flash('Commande annulée avec succès.', 'success')
        return redirect(url_for('commandes.index'))
    return redirect(url_for('commandes.index'))


@commande_routes.route('/details/<int:commande_id>/add', methods=['GET', 'POST'])
def add(commande_id):
    commande = CommandeController.read_one(commande_id)
    if not commande:
        return redirect(url_for('commandes.index'))
    
    if request.method == 'POST':
        produit_id = request.form['produit_id']
        produit = ProduitController.read_one(produit_id)
        if not produit:
            flash('Produit introuvable.', 'error')
            return redirect(url_for('commandes.read_one', commande_id=commande_id))
        
        data = {
            'commande_id': commande_id,
            'produit_id': produit.id,
            'prix_unitaire': produit.prix_vente,
            'quantite': request.form['quantite']
        }
        success, result = CommandeProduitController.add_to_command(data)
        if success:
            flash('Produit ajouté à la commande avec succès.', 'success')
            return redirect(url_for('commandes.read_one', commande_id=commande_id))

    produits = ProduitController.read_all()
    return render_template('commandes/commandes_produits/add.html', commande=commande, produits=produits)
    

@commande_routes.route('/details/<int:commande_id>/edit/<int:commande_produit_id>', methods=['GET', 'POST'])
def update_produit(commande_id, commande_produit_id):
    commande = CommandeController.read_one(commande_id)
    if not commande:
        return redirect(url_for('commandes.index'))
    
    commande_produit = CommandeProduitController.read_one(commande_produit_id)
    if not commande_produit:
        flash('Produit dans la commande introuvable.', 'error')
        return redirect(url_for('commandes.read_one', commande_id=commande_id))

    if request.method == 'POST':
        produit_id = request.form['produit_id']
        produit = ProduitController.read_one(produit_id)
        if not produit:
            flash('Produit introuvable.', 'error')
            return redirect(url_for('commandes.read_one', commande_id=commande_id))
        
        data = {
            'commande_id': commande_id,
            'produit_id': produit.id,
            'prix_unitaire': produit.prix_vente,
            'quantite': request.form['quantite']
        }
        success, result = CommandeProduitController.update(commande_produit_id, data)
        if success:
            flash('Produit mis à jour avec succès.', 'success')
            return redirect(url_for('commandes.read_one', commande_id=commande_id))
        flash(result, 'error')

    produits = ProduitController.read_all()
    return render_template('commandes/commandes_produits/edit.html', commande=commande, commande_produit=commande_produit, produits=produits)

@commande_routes.route('/details/<int:commande_id>/remove/<int:commande_produit_id>')
def delete_produit(commande_id, commande_produit_id):
    success, result = CommandeProduitController.delete(commande_produit_id)
    if success:
        flash('Produit supprimé de la commande avec succès.', 'success')
    else:
        flash(result, 'error')
    return redirect(url_for('commandes.read_one', commande_id=commande_id))
