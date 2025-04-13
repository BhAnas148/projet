from flask import Blueprint, render_template, request, redirect, url_for

from src.controllers.UserController import UserController

commercial_routes = Blueprint('commercial', __name__, url_prefix='/commerciaux')

@commercial_routes.route('/')
def index():
    commerciaux = UserController.read_all_by_role('commercial')
    return render_template('commerciaux/index.html', commerciaux=commerciaux)

@commercial_routes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'email': request.form['email'],
            'mot_de_passe': request.form['mot_de_passe'],
            'role': 'commercial'
        }
        success, result = UserController.create(data)
        if success:
            return redirect(url_for('commercial.index'))
        return render_template('commerciaux/create.html', error=result)
    return render_template('commerciaux/create.html')

@commercial_routes.route('/<int:user_id>')
def read_one(user_id):
    user = UserController.read_one(user_id)
    if user:
        return render_template('commerciaux/detail.html', user=user)
    return redirect(url_for('commercial.index'))

@commercial_routes.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = UserController.read_one(user_id)
    if not user:
        return redirect(url_for('commercial.index'))

    if request.method == 'POST':
        data = {
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'email': request.form['email'],
            'mot_de_passe': request.form['mot_de_passe']
        }
        success, result = UserController.update(user_id, data)
        if success:
            return redirect(url_for('commercial.read_one', user_id=user_id))
        return render_template('commerciaux/update.html', error=result, user=user)

    return render_template('commerciaux/update.html', user=user)

@commercial_routes.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    success, result = UserController.delete(user_id)
    if success:
        return redirect(url_for('commercial.index'))
    return redirect(url_for('commercial.index'))
