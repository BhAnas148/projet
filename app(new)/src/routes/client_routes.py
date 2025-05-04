from flask import Blueprint, render_template, request, redirect, url_for
from src.controllers.UserController import UserController

client_routes = Blueprint(
    'client', __name__, url_prefix='/clients')


@client_routes.route('/')
def index():
    clients = UserController.get_users_by_role('client')
    return render_template('clients/index.html', clients=clients)


@client_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form.get('prenom', ''),
            'date_de_naissance': request.form.get('date_de_naissance', '1990-05-08'),
            'telephone': request.form['telephone'],
            'ville': request.form['ville'],
            'adresse': request.form['adresse'],
            'email': request.form['email'],
            'mot_de_passe': request.form.get('mot_de_passe', ''),
            'role': 'client'
        }
        success, result = UserController.create(data)
        if success:
            return redirect(url_for('client.index'))
        return render_template('clients/create.html', error=result)
    return render_template('clients/create.html')


@client_routes.route('/<int:user_id>')
def read_one(user_id):
    user = UserController.read_one(user_id)
    if user:
        return render_template('clients/details.html', user=user)
    return redirect(url_for('client.index'))


@client_routes.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = UserController.read_one(user_id)
    if not user:
        return redirect(url_for('client.index'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form.get('prenom', ''),
            'date_de_naissance': request.form.get('date_de_naissance', '1990-05-08'),
            'telephone': request.form['telephone'],
            'ville': request.form['ville'],
            'adresse': request.form['adresse'],
            'email': request.form['email'],
            'mot_de_passe': request.form.get('mot_de_passe', ''),
            'role': 'client'
        }
        success, result = UserController.update(user_id, data)
        if success:
            return redirect(url_for('client.read_one', user_id=user_id))
        return render_template('clients/update.html', error=result, user=user)

    return render_template('clients/update.html', user=user)


@client_routes.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    success, result = UserController.delete(user_id)
    if success:
        return redirect(url_for('client.index'))
    return redirect(url_for('client.index'))