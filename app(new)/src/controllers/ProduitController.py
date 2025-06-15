from src.entities import db
from src.entities.produit import Produit
from src.entities.categorie import Categorie
from src.entities.sous_categorie import SousCategorie
from src.entities.image import Image


class ProduitController:

    @staticmethod
    def create(data):
        # Validate categorie
        if not Categorie.query.get(data['categorie_id']):
            return False, "Catégorie non valide"

        # Validate sous-categorie
        if not SousCategorie.query.get(data['sous_categorie_id']):
            return False, "Sous-catégorie non valide"

        produit = Produit(
            designation=data['designation'],
            description=data.get('description', ''),
            prix_vente=data['prix_vente'],
            categorie_id=data['categorie_id'],
            sous_categorie_id=data['sous_categorie_id']
        )
        db.session.add(produit)
        db.session.commit()

        # Add a single primary image
        image = Image(
            produit_id=produit.id,
            nom=data['image_nom'],  # should come from the form
            is_primary=True
        )
        db.session.add(image)
        db.session.commit()

        return True, produit

    @staticmethod
    def read_all():
        return Produit.query.all()

    @staticmethod
    def read_by_sous_categorie(sous_categorie_id):
        return Produit.query.filter_by(sous_categorie_id=sous_categorie_id).all()

    @staticmethod
    def read_by_categorie(categorie_id):
        return Produit.query.filter_by(categorie_id=categorie_id).all()


    @staticmethod
    def read_one(produit_id):
        return Produit.query.get(produit_id)

    @staticmethod
    def update(produit_id, data):
        produit = Produit.query.get(produit_id)
        if not produit:
            return False, "Produit introuvable"

        # Validate category if being updated
        if data.get('categorie_id'):
            if not Categorie.query.get(data['categorie_id']):
                return False, "Catégorie non valide"
            produit.categorie_id = data['categorie_id']

        # Validate subcategory if being updated
        if data.get('sous_categorie_id'):
            if not SousCategorie.query.get(data['sous_categorie_id']):
                return False, "Sous-catégorie non valide"
            produit.sous_categorie_id = data['sous_categorie_id']

        # Update basic product info
        produit.designation = data.get('designation', produit.designation)
        produit.description = data.get('description', produit.description)
        produit.prix_vente = data.get('prix_vente', produit.prix_vente)

        # Handle image update if new image was provided
        if 'image_nom' in data:
            # Find existing primary image
            primary_image = Image.query.filter_by(
                produit_id=produit.id,
                is_primary=True
            ).first()

            if primary_image:
                # Update existing primary image
                primary_image.nom = data['image_nom']
            else:
                # Create new primary image if none exists
                new_image = Image(
                    produit_id=produit.id,
                    nom=data['image_nom'],
                    is_primary=True
                )
                db.session.add(new_image)

        db.session.commit()
        return True, produit

    @staticmethod
    def delete(produit_id):
        produit = Produit.query.get(produit_id)
        if not produit:
            return False, "Produit introuvable"

        # Optionally delete associated images
        Image.query.filter_by(produit_id=produit.id).delete()

        db.session.delete(produit)
        db.session.commit()
        return True, "Produit supprimé"