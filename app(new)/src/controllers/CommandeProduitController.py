from src.entities import db
from src.entities.commande_produit import CommandeProduit


class CommandeProduitController:

    @staticmethod
    def add_to_command(data):
        # Create a new CommandeProduit entry
        commande_produit = CommandeProduit(
            commande_id=data['commande_id'],
            produit_id=data['produit_id'],
            prix_unitaire=data['prix_unitaire'],
            quantite=data['quantite'],
            prix_total=data['prix_unitaire'] * data['quantite']
        )
        db.session.add(commande_produit)
        db.session.commit()
        return True, commande_produit

    @staticmethod
    def read_all():
        return CommandeProduit.query.all()

    @staticmethod
    def read_one(commande_produit_id):
        return CommandeProduit.query.get(commande_produit_id)

    @staticmethod
    def update(commande_produit_id, data):
        commande_produit = CommandeProduit.query.get(commande_produit_id)
        if not commande_produit:
            return False, "Produit dans la commande introuvable"

        # Update the fields with the new data if provided
        if data.get('quantite') and data['quantite'] != commande_produit.quantite:
            commande_produit.quantite = data['quantite']
            commande_produit.prix_total = commande_produit.quantite * \
                commande_produit.prix_unitaire

        if data.get('prix_unitaire') and data['prix_unitaire'] != commande_produit.prix_unitaire:
            commande_produit.prix_unitaire = data['prix_unitaire']
            commande_produit.prix_total = commande_produit.quantite * \
                commande_produit.prix_unitaire

        db.session.commit()
        return True, commande_produit

    @staticmethod
    def delete(commande_produit_id):
        commande_produit = CommandeProduit.query.get(commande_produit_id)
        if not commande_produit:
            return False, "Produit dans la commande introuvable"

        db.session.delete(commande_produit)
        db.session.commit()
        return True, "Produit supprimé de la commande"
