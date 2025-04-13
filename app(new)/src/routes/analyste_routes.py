from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.UserController import UserController

analyste_routes = Blueprint('analyste', __name__, url_prefix='/analystes')

@analyste_routes.route('/')
def index():
    analystes = UserController.read_all_by_role('analyste')
    return render_template('analystes/index.html', analystes=analystes)

@analyste_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'email': request.form['email'],
            'mot_de_passe': request.form['mot_de_passe'],
            'role': 'analyste'
        }
        success, result = UserController.create(data)
        if success:
            return redirect(url_for('analyste.index'))
        return render_template('analystes/create.html', error=result)
    return render_template('analystes/create.html')

@analyste_routes.route('/<int:user_id>')
def read_one(user_id):
    user = UserController.read_one(user_id)
    if user:
        return render_template('analystes/detail.html', user=user)
    return redirect(url_for('analyste.index'))

@analyste_routes.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = UserController.read_one(user_id)
    if not user:
        return redirect(url_for('analyste.index'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'email': request.form['email'],
            'mot_de_passe': request.form['mot_de_passe']
        }
        success, result = UserController.update(user_id, data)
        if success:
            return redirect(url_for('analyste.read_one', user_id=user_id))
        return render_template('analystes/update.html', error=result, user=user)

    return render_template('analystes/update.html', user=user)

@analyste_routes.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    success, result = UserController.delete(user_id)
    if success:
        return redirect(url_for('analyste.index'))
    return redirect(url_for('analyste.index'))  # Handle error if necessary
