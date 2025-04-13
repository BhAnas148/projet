from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.CommandeController import CommandeController

commande_routes = Blueprint(
    'commande', __name__, url_prefix='/commandes')


@commande_routes.route('/')
def index():
    commandes = CommandeController.read_all()
    return render_template('commandes/index.html', commandes=commandes)


@commande_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'client_id': request.form['client_id'],
            'montant_total': request.form['montant_total'],
            'nb_article': request.form['nb_article']
        }
        success, result = CommandeController.create(data)
        if success:
            return redirect(url_for('commandes.index'))
        return render_template('commandes/create.html', error=result)

    return render_template('commandes/create.html')


@commande_routes.route('/<int:commande_id>')
def read_one(commande_id):
    commande = CommandeController.read_one(commande_id)
    if commande:
        return render_template('commandes/detail.html', commande=commande)
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


@commande_routes.route('/delete/<int:commande_id>', methods=['POST'])
def delete(commande_id):
    success, result = CommandeController.delete(commande_id)
    if success:
        return redirect(url_for('commandes.index'))
    return redirect(url_for('commandes.index'))  # Handle error if necessary
