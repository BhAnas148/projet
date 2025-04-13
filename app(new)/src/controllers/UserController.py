from werkzeug.security import generate_password_hash, check_password_hash

from src.entities import db
from src.entities.user import User


class UserController:

    @staticmethod
    def create(data):
        if User.query.filter_by(email=data['email']).first():
            return False, "Email already exists"

        if User.query.filter_by(telephone=data['telephone']).first():
            return False, "Telephone already exists"

        user = User(
            nom=data['nom'],
            prenom=data['prenom'],
            date_naissance=data['date_naissance'],
            telephone=data['telephone'],
            ville=data['ville'],
            adresse=data['adresse'],
            email=data['email'],
            mot_de_passe=generate_password_hash(data['mot_de_passe']),
            role=data['role']
        )
        db.session.add(user)
        db.session.commit()
        return True, user

    @staticmethod
    def read_all():
        return User.query.all()

    @staticmethod
    def read_one(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"

        if data.get('email') and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return False, "Email already exists"
            user.email = data['email']

        if data.get('telephone') and data['telephone'] != user.telephone:
            if User.query.filter_by(telephone=data['telephone']).first():
                return False, "Telephone already exists"
            user.telephone = data['telephone']

        user.nom = data.get('nom', user.nom)
        user.prenom = data.get('prenom', user.prenom)
        user.date_naissance = data.get('date_naissance', user.date_naissance)
        user.ville = data.get('ville', user.ville)
        user.adresse = data.get('adresse', user.adresse)
        user.role = data.get('role', user.role)

        db.session.commit()
        return True, user

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        db.session.delete(user)
        db.session.commit()
        return True, "User deleted"

    @staticmethod
    def login(email, mot_de_passe):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.mot_de_passe, mot_de_passe):
            return True, user
        return False, "Invalid credentials"
