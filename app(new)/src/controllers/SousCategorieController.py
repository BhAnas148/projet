from src.entities import db
from src.entities.categorie import Categorie
from src.entities.sous_categorie import SousCategorie


class SousCategorieController:

    @staticmethod
    def create(data):
        if 'categorie_id' not in data or not Categorie.query.get(data['categorie_id']):
            return False, "Catégorie non valide"

        if SousCategorie.query.filter_by(nom=data['nom'], categorie_id=data['categorie_id']).first():
            return False, "Sous-catégorie déjà existante dans cette catégorie"

        sous_categorie = SousCategorie(
            nom=data['nom'],
            categorie_id=data['categorie_id']
        )
        db.session.add(sous_categorie)
        db.session.commit()
        return True, sous_categorie

    @staticmethod
    def read_all():
        return SousCategorie.query.all()

    @staticmethod
    def read_one(sous_categorie_id):
        return SousCategorie.query.get(sous_categorie_id)

    @staticmethod
    def update(sous_categorie_id, data):
        sous_categorie = SousCategorie.query.get(sous_categorie_id)
        if not sous_categorie:
            return False, "Sous-catégorie introuvable"

        if data.get('categorie_id'):
            if not Categorie.query.get(data['categorie_id']):
                return False, "Catégorie non valide"
            sous_categorie.categorie_id = data['categorie_id']

        if data.get('nom'):
            # Check uniqueness within the same category
            exists = SousCategorie.query.filter_by(
                nom=data['nom'],
                categorie_id=sous_categorie.categorie_id
            ).first()
            if exists and exists.id != sous_categorie.id:
                return False, "Nom déjà utilisé dans cette catégorie"
            sous_categorie.nom = data['nom']

        db.session.commit()
        return True, sous_categorie

    @staticmethod
    def delete(sous_categorie_id):
        sous_categorie = SousCategorie.query.get(sous_categorie_id)
        if not sous_categorie:
            return False, "Sous-catégorie introuvable"

        db.session.delete(sous_categorie)
        db.session.commit()
        return True, "Sous-catégorie supprimée"
