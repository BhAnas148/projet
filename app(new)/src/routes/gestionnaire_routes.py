from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.UserController import UserController

gestionnaire_routes = Blueprint(
    'gestionnaire', __name__, url_prefix='/gestionnaires')


@gestionnaire_routes.route('/')
def index():
    gestionnaires = UserController.read_all_by_role('gestionnaire')
    return render_template('gestionnaires/index.html', gestionnaires=gestionnaires)


@gestionnaire_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'email': request.form['email'],
            'mot_de_passe': request.form['mot_de_passe'],
            'role': 'gestionnaire'
        }
        success, result = UserController.create(data)
        if success:
            return redirect(url_for('gestionnaire.index'))
        return render_template('gestionnaires/create.html', error=result)
    return render_template('gestionnaires/create.html')


@gestionnaire_routes.route('/<int:user_id>')
def read_one(user_id):
    user = UserController.read_one(user_id)
    if user:
        return render_template('gestionnaires/detail.html', user=user)
    return redirect(url_for('gestionnaire.index'))


@gestionnaire_routes.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = UserController.read_one(user_id)
    if not user:
        return redirect(url_for('gestionnaire.index'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'email': request.form['email'],
            'mot_de_passe': request.form['mot_de_passe']
        }
        success, result = UserController.update(user_id, data)
        if success:
            return redirect(url_for('gestionnaire.read_one', user_id=user_id))
        return render_template('gestionnaires/update.html', error=result, user=user)

    return render_template('gestionnaires/update.html', user=user)


@gestionnaire_routes.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    success, result = UserController.delete(user_id)
    if success:
        return redirect(url_for('gestionnaire.index'))
    return redirect(url_for('gestionnaire.index'))
