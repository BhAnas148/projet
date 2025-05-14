from flask import Blueprint, render_template, request, redirect, url_for
from src.controllers.UserController import UserController
from src.entities.user import UserRole

client_routes = Blueprint(
    'client', __name__, url_prefix='/client'
)


@client_routes.route('/')
def index():
    client = UserController.get_users_by_role('client')
    return render_template('client/index.html', client=client)


@client_routes.route('/create', methods=['GET', 'POST'])
def create():
    show_password = True
    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'date_de_naissance': request.form.get('date_de_naissance'),
            'telephone': request.form['telephone'],
            'ville': request.form['ville'],
            'adresse': request.form['adresse'],
            'email': request.form['email'],
            'mot_de_passe': request.form['mot_de_passe'],
            'role': 'client'
        }
        success, result = UserController.create(data)
        if success:
            return redirect(url_for('client.index'))
        
        return render_template('client/create.html', error=result, show_password=show_password)
    
    return render_template('client/create.html', show_password=show_password)


@client_routes.route('/<int:user_id>')
def read_one(user_id):
    user = UserController.read_one(user_id)
    
    if user and user.role == UserRole.client:
        return render_template('client/details.html', user=user)
    return redirect(url_for('client.index'))


@client_routes.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = UserController.read_one(user_id)
    if not user or user.role != UserRole.client:
        return redirect(url_for('client.index'))

    if request.method == 'POST':
        data = {
             'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'date_de_naissance': request.form.get('date_de_naissance'),
            'telephone': request.form['telephone'],
            'ville': request.form['ville'],
            'adresse': request.form['adresse'],
            'email': request.form['email'],
            'role': 'client'
        }
        success, result = UserController.update(user_id, data)
        if success:
            return redirect(url_for('client.read_one', user_id=user_id))
        return render_template('client/update.html', error=result, user=user)

    return render_template('client/update.html', user=user)


@client_routes.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    success, result = UserController.delete(user_id)
    if success:
        return redirect(url_for('client.index'))
    return redirect(url_for('client.index'))