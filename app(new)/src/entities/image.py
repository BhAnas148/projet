from . import db


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey(
        'produit.id'), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
