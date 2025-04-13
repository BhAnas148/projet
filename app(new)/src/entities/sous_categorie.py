from . import db


class SousCategorie(db.Model):
    __tablename__ = 'sous_categorie'

    id = db.Column(db.Integer, primary_key=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey(
        'categorie.id'), nullable=False)
    nom = db.Column(db.String(255), nullable=False)

    # Relationships:
    produits = db.relationship('Produit', backref='sous_categorie', lazy=True)
