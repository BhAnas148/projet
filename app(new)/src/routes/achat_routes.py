from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.AchatController import AchatController
from src.controllers.UserController import UserController
from src.controllers.ProduitController import ProduitController

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
        else:
            # En cas d'erreur, on recharge les listes pour le formulaire
            fournisseurs = UserController.get_users_by_role('fournisseur')
            produits = ProduitController.read_all()
            return render_template(
                'achats/create.html',
                error=result,
                fournisseurs=fournisseurs,
                produits=produits
            )

    # GET request
    fournisseurs = UserController.get_users_by_role('fournisseur')
    produits = ProduitController.read_all()
    return render_template(
        'achats/create.html',
        fournisseurs=fournisseurs,
        produits=produits
    )


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

    # Récupération des listes pour le formulaire
    fournisseurs = UserController.get_users_by_role('fournisseur')
    produits = ProduitController.read_all()

    if request.method == 'POST':
        data = {
            'produit_id': request.form['produit_id'],
            'fournisseur_id': request.form['fournisseur_id'],
            'prix_achat_unitaire': request.form['prix_achat_unitaire'],
            'quantite': request.form['quantite']
        }
        success, result = AchatController.update(achat_id, data)
        if success:
            return redirect(url_for('achat.read_one', achat_id=achat_id))
        return render_template(
            'achats/update.html',
            error=result,
            achat=achat,
            fournisseurs=fournisseurs,
            produits=produits
        )

    return render_template(
        'achats/update.html',
        achat=achat,
        fournisseurs=fournisseurs,
        produits=produits
    )


@achat_routes.route('/delete/<int:achat_id>', methods=['POST'])
def delete(achat_id):
    success, result = AchatController.delete(achat_id)
    # Tu peux aussi gérer les erreurs ici avec flash ou message
    return redirect(url_for('achat.index'))
