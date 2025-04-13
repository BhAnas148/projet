from datetime import datetime

from . import db


class Achat(db.Model):
    __tablename__ = 'achat'

    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey(
        'produit.id'), nullable=False)
    fournisseur_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    prix_achat_unitaire = db.Column(db.Float, nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_achat_total = db.Column(db.Float, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
