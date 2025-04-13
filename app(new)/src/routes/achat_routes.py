from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.AchatController import AchatController

achat_routes = Blueprint('achat', __name__, url_prefix='/achats')


@achat_routes.route('/')
def index():
    achats = AchatController.read_all()
    return render_template('achats/index.html', achats=achats)


@achat_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'produit_id': request.form['produit_id'],
            'fournisseur_id': request.form['fournisseur_id'],
            'prix_achat_unitaire': request.form['prix_achat_unitaire'],
            'quantite': request.form['quantite'],
            'date_creation': request.form['date_creation']
        }
        success, result = AchatController.create(data)
        if success:
            return redirect(url_for('achat.index'))
        return render_template('achats/create.html', error=result)

    return render_template('achats/create.html')


@achat_routes.route('/<int:achat_id>')
def read_one(achat_id):
    achat = AchatController.read_one(achat_id)
    if achat:
        return render_template('achats/detail.html', achat=achat)
    return redirect(url_for('achat.index'))


@achat_routes.route('/update/<int:achat_id>', methods=['GET', 'POST'])
def update(achat_id):
    achat = AchatController.read_one(achat_id)
    if not achat:
        return redirect(url_for('achat.index'))
    
    if request.method == 'POST':
        data = {
            'prix_achat_unitaire': request.form['prix_achat_unitaire'],
            'quantite': request.form['quantite']
        }
        success, result = AchatController.update(achat_id, data)
        if success:
            return redirect(url_for('achat.read_one', achat_id=achat_id))
        return render_template('achats/update.html', error=result, achat=achat)

    return render_template('achats/update.html', achat=achat)


@achat_routes.route('/delete/<int:achat_id>', methods=['POST'])
def delete(achat_id):
    success, result = AchatController.delete(achat_id)
    if success:
        return redirect(url_for('achat.index'))
    return redirect(url_for('achat.index'))  # Handle error if necessary
