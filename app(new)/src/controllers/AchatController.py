from datetime import datetime

from src.entities import db
from src.entities.achat import Achat
from src.entities.produit import Produit
from src.entities.user import User, UserRole


class AchatController:

    @staticmethod
    def create(data):
        # Validate produit
        if not Produit.query.get(data['produit_id']):
            return False, "Produit non valide"

        # Validate fournisseur
        print(data['fournisseur_id'])
        fournisseur = User.query.get(data['fournisseur_id'])
        print(not fournisseur)
        print(fournisseur.role)
        if not fournisseur or fournisseur.role != UserRole.fournisseur:
            return False, "Fournisseur non valide"

        prix_total = int(data['prix_achat_unitaire']) * int(data['quantite'])

        achat = Achat(
            produit_id=data['produit_id'],
            fournisseur_id=data['fournisseur_id'],
            prix_achat_unitaire=data['prix_achat_unitaire'],
            quantite=data['quantite'],
            prix_achat_total=prix_total,
            date_creation=data.get('date_creation', datetime.utcnow())
        )

        db.session.add(achat)
        db.session.commit()
        return True, achat

    @staticmethod
    def read_all():
        return Achat.query.all()

    @staticmethod
    def read_one(achat_id):
        return Achat.query.get(achat_id)

    @staticmethod
    def update(achat_id, data):
        achat = Achat.query.get(achat_id)
        if not achat:
            return False, "Achat introuvable"

        if data.get('produit_id'):
            if not Produit.query.get(data['produit_id']):
                return False, "Produit non valide"
            achat.produit_id = data['produit_id']

        if data.get('fournisseur_id'):
            fournisseur = User.query.get(data['fournisseur_id'])
            if not fournisseur or fournisseur.role != "fournisseur":
                return False, "Fournisseur non valide"
            achat.fournisseur_id = data['fournisseur_id']

        achat.prix_achat_unitaire = data.get(
            'prix_achat_unitaire', achat.prix_achat_unitaire)
        achat.quantite = data.get('quantite', achat.quantite)

        # Recalculate total
        achat.prix_achat_total = achat.prix_achat_unitaire * achat.quantite

        if data.get('date_creation'):
            achat.date_creation = data['date_creation']

        db.session.commit()
        return True, achat

    @staticmethod
    def delete(achat_id):
        achat = Achat.query.get(achat_id)
        if not achat:
            return False, "Achat introuvable"

        db.session.delete(achat)
        db.session.commit()
        return True, "Achat supprimé"
