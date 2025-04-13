import enum

from . import db


class UserRole(enum.Enum):
    client = "client"
    fournisseur = "fournisseur"
    analyste = "analyste"
    gestionnaire = "gestionnaire"
    commercial = "commercial"
    administrateur = "administrateur"


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_de_naissance = db.Column(db.Date, nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    ville = db.Column(db.String(100), nullable=True)
    adresse = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    mot_de_passe = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    # Relationships:
    # A user with role 'client' can have many commandes.
    commandes = db.relationship(
        'Commande', backref='client', lazy=True, foreign_keys='Commande.client_id')
    # A user with role 'fournisseur' can have many achats.
    achats = db.relationship(
        'Achat', backref='fournisseur', lazy=True, foreign_keys='Achat.fournisseur_id')
