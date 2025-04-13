from datetime import datetime

from . import db


class Commande(db.Model):
    __tablename__ = 'commande'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    montant_total = db.Column(db.Float, nullable=False)
    nb_article = db.Column(db.Integer, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships:
    commande_produits = db.relationship(
        'CommandeProduit', backref='commande', lazy=True)
    