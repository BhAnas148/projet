from . import db




class Categorie(db.Model):
    __tablename__ = 'categorie'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)

    # Relationships:
    sous_categories = db.relationship(
        'SousCategorie', backref='categorie', lazy=True)
    produits = db.relationship('Produit', backref='categorie', lazy=True)
