from flask import Blueprint, render_template, request, redirect, url_for
from src.controllers.UserController import UserController

commercial_routes = Blueprint(
    'commercial', __name__, url_prefix='/commercial'
)


@commercial_routes.route('/')
def index():
    commercials = UserController.read_all()
    return render_template('commercial/index.html', commercials=commercials)


@commercial_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form.get('prenom', ''),
            'date_de_naissance': request.form.get('date_de_naissance', '1990-01-01'),
            'telephone': request.form['telephone'],
            'ville': request.form['ville'],
            'adresse': request.form['adresse'],
            'email': request.form['email'],
            'mot_de_passe': '',
            'role': 'commercial'
        }
        success, result = UserController.create(data)
        if success:
            return redirect(url_for('commercial.index'))
        return render_template('commercial/create.html', error=result)
    return render_template('commercial/create.html')


@commercial_routes.route('/<int:user_id>')
def read_one(user_id):
    user = UserController.read_one(user_id)
    if user and user['role'] == 'commercial':
        return render_template('commercial/details.html', user=user)
    return redirect(url_for('commercial.index'))


@commercial_routes.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = UserController.read_one(user_id)
    if not user or user['role'] != 'commercial':
        return redirect(url_for('commercial.index'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form.get('prenom', ''),
            'date_de_naissance': request.form.get('date_de_naissance', '1990-01-01'),
            'telephone': request.form['telephone'],
            'ville': request.form['ville'],
            'adresse': request.form['adresse'],
            'email': request.form['email'],
            'mot_de_passe': '',
            'role': 'commercial'
        }
        success, result = UserController.update(user_id, data)
        if success:
            return redirect(url_for('commercial.read_one', user_id=user_id))
        return render_template('commercial/update.html', error=result, user=user)

    return render_template('commercial/update.html', user=user)


@commercial_routes.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    success, result = UserController.delete(user_id)
    if success:
        return redirect(url_for('commercial.index'))
    return redirect(url_for('commercial.index'))