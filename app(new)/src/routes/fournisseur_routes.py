from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.controllers.UserController import UserController
from src.controllers.AchatController import AchatController

fournisseur_routes = Blueprint(
    'fournisseur', __name__, url_prefix='/fournisseur')


@fournisseur_routes.route('/')
def index():
    fournisseur = UserController.get_users_by_role('fournisseur')
    return render_template('fournisseur/index.html', fournisseur=fournisseur)


@fournisseur_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': '',
            'date_de_naissance': '1990-05-08',
            'telephone': request.form['telephone'],
            'ville': request.form['ville'],
            'adresse': request.form['adresse'],
            'email': request.form['email'],
            'mot_de_passe': '',
            'role': 'fournisseur'
        }
        success, result = UserController.create(data)
        if success:
            return redirect(url_for('fournisseur.index'))
        return render_template('fournisseur/create.html', error=result)
    return render_template('fournisseur/create.html')


@fournisseur_routes.route('/<int:user_id>')
def read_one(user_id):
    user = UserController.read_one(user_id)
    if user:
        return render_template('fournisseur/details.html', user=user)
    return redirect(url_for('fournisseur.index'))


@fournisseur_routes.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = UserController.read_one(user_id)
    if not user:
        return redirect(url_for('fournisseur.index'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'telephone': request.form['telephone'],
            'ville': request.form['ville'],
            'adresse': request.form['adresse'],
            'email': request.form['email'],

            'prenom': '',
            'date_de_naissance': '1990-05-08',
            'mot_de_passe': '',
            'role': 'fournisseur'
        }
        success, result = UserController.update(user_id, data)
        if success:
            return redirect(url_for('fournisseur.read_one', user_id=user_id))
        return render_template('fournisseur/update.html', error=result, user=user)

    return render_template('fournisseur/update.html', user=user)


@fournisseur_routes.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    # check if fournisseur has any achats
    achats = AchatController.get_achats_by_fournisseur(user_id)
    if achats:
        flash('Cannot delete fournisseur with existing achats', 'danger')
        return redirect(url_for('fournisseur.index'))

    success, result = UserController.delete(user_id)
    if success:
        return redirect(url_for('fournisseur.index'))
    return redirect(url_for('fournisseur.index'))