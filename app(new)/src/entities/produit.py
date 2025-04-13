from . import db


class Produit(db.Model):
    __tablename__ = 'produit'

    id = db.Column(db.Integer, primary_key=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    sous_categorie_id = db.Column(db.Integer, db.ForeignKey('sous_categorie.id'), nullable=True)
    designation = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    prix_vente = db.Column(db.Float, nullable=False)

    # Relationships:
    images = db.relationship('Image', backref='produit', lazy=True)
    commande_produits = db.relationship('CommandeProduit', backref='produit', lazy=True)
    achats = db.relationship('Achat', backref='produit', lazy=True)