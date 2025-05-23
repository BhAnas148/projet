from flask import Blueprint, render_template, url_for, redirect, request, flash, session

from src.controllers.UserController import UserController

user_routes = Blueprint('users', __name__)


@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserController.login(email, password)
        
        if user:
            session['LOGGED_IN'] = True
            session['user_id'] = user.id
            session['user_role'] = user.role.value
            session['user_name'] = user.nom
            session['user_prenom'] = user.prenom
            return redirect(url_for('home.home'))
        else:
            flash('l\'email et/ou le mot de passe sont incorrects', 'danger')
            return redirect(url_for('users.login'))

    return render_template('login.html')

@user_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))