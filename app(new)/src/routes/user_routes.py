from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from src.controllers.UserController import UserController
from src.entities.user import User, UserRole

user_routes = Blueprint('users', __name__)


@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserController.login(email, password)

        print(user.role)
        if user:  # Si authentification réussie
            session['LOGGED_IN'] = True
            session['user_id'] = user.id
            session['user_role'] = user.role.value
            session['user_name'] = user.nom
            session['user_prenom'] = user.prenom

            if user.role in [UserRole.administrateur, UserRole.commercial]:
                return redirect(url_for('commandes.index'))

            return redirect(url_for('home.home'))
        else:
            flash("Identifiants invalides", 'danger')
            return redirect(url_for('users.login'))

    return render_template('login.html')


@user_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))


@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Validation des données (sans confirm_password)
        required_fields = {
            'nom': "Le nom est obligatoire",
            'prenom': "Le prénom est obligatoire",
            'email': "L'email est obligatoire",
            'mot_de_passe': "Le mot de passe est obligatoire",
            'date_de_naissance': "La date de naissance est obligatoire",
            'telephone': "Le téléphone est obligatoire",
            'ville': "La ville est obligatoire",
            'adresse': "L'adresse est obligatoire"
        }

        errors = []
        user_data = {}

        for field, error_msg in required_fields.items():
            value = request.form.get(field)
            if not value:
                errors.append(error_msg)
            user_data[field] = value

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('users.register'))

        # Préparation des données pour le contrôleur
        controller_data = {
            'nom': user_data['nom'],
            'prenom': user_data['prenom'],
            'email': user_data['email'],
            'mot_de_passe': user_data['mot_de_passe'],
            'date_de_naissance': user_data['date_de_naissance'],
            'telephone': user_data['telephone'],
            'ville': user_data['ville'],
            'adresse': user_data['adresse'],
            'role': 'client'  # Rôle par défaut
        }

        # Création de l'utilisateur
        success, result = UserController.create(controller_data)

        if success:
            flash(
                "Compte créé avec succès. Vous pouvez maintenant vous connecter.", 'success')
            return redirect(url_for('users.login'))
        else:
            flash(result if isinstance(result, str)
                  else "Erreur lors de la création du compte", 'danger')
            return redirect(url_for('users.register'))

    return render_template('register.html')
