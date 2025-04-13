from . import db


class CommandeProduit(db.Model):
    __tablename__ = 'commande_produit'
    
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_total = db.Column(db.Float, nullable=False)