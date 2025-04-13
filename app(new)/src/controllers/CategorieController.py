from src.entities import db
from src.entities.categorie import Categorie


class CategorieController:

    @staticmethod
    def create(data):
        if Categorie.query.filter_by(nom=data['nom']).first():
            return False, "Catégorie déjà existante"

        categorie = Categorie(nom=data['nom'])
        db.session.add(categorie)
        db.session.commit()
        return True, categorie

    @staticmethod
    def read_all():
        return Categorie.query.all()

    @staticmethod
    def read_one(categorie_id):
        return Categorie.query.get(categorie_id)

    @staticmethod
    def update(categorie_id, data):
        categorie = Categorie.query.get(categorie_id)
        if not categorie:
            return False, "Catégorie introuvable"

        if data.get('nom') and data['nom'] != categorie.nom:
            if Categorie.query.filter_by(nom=data['nom']).first():
                return False, "Nom déjà utilisé"
            categorie.nom = data['nom']

        db.session.commit()
        return True, categorie

    @staticmethod
    def delete(categorie_id):
        categorie = Categorie.query.get(categorie_id)
        if not categorie:
            return False, "Catégorie introuvable"

        db.session.delete(categorie)
        db.session.commit()
        return True, "Catégorie supprimée"
