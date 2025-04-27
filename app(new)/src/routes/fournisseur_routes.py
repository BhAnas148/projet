from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.UserController import UserController

from src.entities.user import UserRole

fournisseur_routes = Blueprint(
    'fournisseur', __name__, url_prefix='/fournisseurs')


@fournisseur_routes.route('/')
def index():
    fournisseurs = UserController.read_all()
    return render_template('fournisseurs/index.html', fournisseurs=fournisseurs)


@fournisseur_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
          
            'nom' : request.form['nom'],
            'prenom' : '',
            'date_de_naissance' : '1900-01-01',
            'telephone' : request.form['telephone'],
            'ville' : request.form['ville'],
            'adresse' : request.form['adresse'],
            'email' : request.form['email'],
            'mot_de_passe' : '',
            'role' : 'fournisseur'
        }
        success, result = UserController.create(data)
        if success:
            return redirect(url_for('fournisseur.index'))
        return render_template('fournisseurs/create.html', error=result)
    return render_template('fournisseurs/create.html')


@fournisseur_routes.route('/<int:user_id>')
def read_one(user_id):
    user = UserController.read_one(user_id)
    if user:
        return render_template('fournisseurs/detail.html', user=user)
    return redirect(url_for('fournisseur.index'))


@fournisseur_routes.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = UserController.read_one(user_id)
    if not user:
        return redirect(url_for('fournisseur.index'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'email': request.form['email'],
            'mot_de_passe': request.form['mot_de_passe']
        }
        success, result = UserController.update(user_id, data)
        if success:
            return redirect(url_for('fournisseur.read_one', user_id=user_id))
        return render_template('fournisseurs/update.html', error=result, user=user)

    return render_template('fournisseurs/update.html', user=user)


@fournisseur_routes.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    success, result = UserController.delete(user_id)
    if success:
        return redirect(url_for('fournisseur.index'))
    return redirect(url_for('fournisseur.index'))
