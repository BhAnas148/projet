from datetime import datetime
from src.entities import db
from src.entities.image import Image

class ImageController:

    # Create
    @staticmethod
    def create(produit_id, nom, is_primary=False):
        """Create a new image record"""
        image = Image(
            produit_id=produit_id,
            nom=nom,
            is_primary=is_primary
        )
        db.session.add(image)
        db.session.commit()
        return image

    # Update
    @staticmethod
    def update(image_id, nom=None, is_primary=None):
        """Update an existing image"""
        image = Image.query.get(image_id)
        if not image:
            return None

        if nom is not None:
            image.nom = nom
        if is_primary is not None:
            image.is_primary = is_primary
            
        db.session.commit()
        return image

    # Delete
    @staticmethod
    def delete(image_id):
        """Delete an image record"""
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()
            return True
        return False

    # Read All
    @staticmethod
    def read_all(produit_id):
        """Get all images for a product"""
        return Image.query.filter_by(produit_id=produit_id).all()

    # Read One
    @staticmethod
    def read_one(image_id):
        """Get a single image by ID"""
        return Image.query.get(image_id)

    # Read Primary
    @staticmethod
    def read_primary(produit_id):
        """Get the primary image for a product"""
        return Image.query.filter_by(
            produit_id=produit_id,
            is_primary=True
        ).first()

    # Update Selection
    @staticmethod
    def update_selection(produit_id, image_id=None):
        """Set primary image (similar to your update_selection)"""
        images = ImageController.read_all(produit_id)
        
        if not images:
            return None

        # If no image_id provided, use the first one
        if image_id is None:
            image_id = images[0].id

        # Reset all primary flags
        Image.query.filter_by(produit_id=produit_id).update({'is_primary': False})
        
        # Set the new primary image
        primary_image = Image.query.get(image_id)
        if primary_image:
            primary_image.is_primary = True
            db.session.commit()
        
        return primary_image

    # Count Primary
    @staticmethod
    def count_primary(produit_id):
        """Count how many primary images exist for a product"""
        return Image.query.filter_by(
            produit_id=produit_id,
            is_primary=True
        ).count()
    
    @staticmethod
    def set_primary(produit_id, image_id):
        """Set an image as primary and demote others"""
        try:
            # First get the image we want to set as primary
            new_primary = Image.query.filter_by(
                id=image_id,
                produit_id=produit_id
            ).first()
            
            if not new_primary:
                return False, "Image non trouvée"

            # Demote all other primary images for this product
            Image.query.filter_by(
                produit_id=produit_id,
                is_primary=True
            ).update({'is_primary': False})
            
            # Promote the selected image
            new_primary.is_primary = True
            db.session.commit()
            
            return True, new_primary
        except Exception as e:
            db.session.rollback()
            return False, str(e)