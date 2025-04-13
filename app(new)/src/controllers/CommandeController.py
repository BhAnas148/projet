from src.entities import db
from src.entities.commande import Commande


class CommandeController:

    @staticmethod
    def create(data):
        # Create the new command
        commande = Commande(
            client_id=data['client_id'],
            montant_total=data['montant_total'],
            nb_article=data['nb_article']
        )
        db.session.add(commande)
        db.session.commit()
        return True, commande

    @staticmethod
    def read_all():
        return Commande.query.all()

    @staticmethod
    def read_one(commande_id):
        return Commande.query.get(commande_id)

    @staticmethod
    def update(commande_id, data):
        commande = Commande.query.get(commande_id)
        if not commande:
            return False, "Commande introuvable"

        # Update fields if provided
        if data.get('client_id') and data['client_id'] != commande.client_id:
            commande.client_id = data['client_id']
        if data.get('montant_total') and data['montant_total'] != commande.montant_total:
            commande.montant_total = data['montant_total']
        if data.get('nb_article') and data['nb_article'] != commande.nb_article:
            commande.nb_article = data['nb_article']

        db.session.commit()
        return True, commande

    @staticmethod
    def delete(commande_id):
        commande = Commande.query.get(commande_id)
        if not commande:
            return False, "Commande introuvable"

        db.session.delete(commande)
        db.session.commit()
        return True, "Commande supprimée"
